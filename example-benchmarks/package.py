#!/usr/bin/env python3

from __future__ import annotations

import json
import shlex
import tarfile
from tarfile import TarFile, TarInfo
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from glob import iglob
from io import BytesIO
from itertools import chain, tee
from json import dumps
from pathlib import Path, PosixPath, PurePosixPath
from typing import cast, TypeVar

from cmakelang.lex import tokenize
from cmakelang.parse import parse
from cmakelang.parse.argument_nodes import PositionalGroupNode
from cmakelang.parse.body_nodes import BodyNode, StatementNode, TreeNode
from cmakelang.parse.statement_node import FunctionNameNode

DUMUX_VERSION = "3.9.0"

_T = TypeVar("_T")


def zip_with_next(iterable: Iterable[_T]) -> Iterable[tuple[_T, _T]]:
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse_file(file: str) -> BodyNode:
    with open(file) as f:
        raw = f.read()
    tokens = tokenize(raw)
    return parse(tokens)


def get_added_tests(tree: BodyNode) -> list[StatementNode]:
    return [
        node
        for node in tree.children
        if isinstance(node, StatementNode)
        and get_function_name_or_none(node) == "dumux_add_test"
    ]


def get_function_name_or_none(node: StatementNode) -> str | None:
    child = node.children[0]
    if isinstance(child, FunctionNameNode):
        return child.children[0].content
    else:
        return None


@dataclass
class AddTest:
    name: str
    labels: list[str]
    command: str
    command_args: list[str]


def parse_add_test(node: StatementNode) -> AddTest:
    parameters = flatten_group(get_group_of_function(node))

    indexed_params = [
        (idx, param) for (idx, param) in enumerate(parameters) if param.isupper()
    ] + [(len(parameters), None)]
    named_parameters = {
        param: parameters[start + 1 : end]
        for ((start, param), (end, _)) in zip_with_next(indexed_params)
    }

    name = named_parameters["NAME"]
    if len(name) != 1:
        raise ValueError(f"more than one NAME: {name}")
    name = name[0]
    labels = named_parameters["LABELS"]
    command = named_parameters["COMMAND"]
    if len(command) != 1:
        raise ValueError(f"more than one COMMAND: {command}")
    command = command[0]
    command_args = named_parameters["CMD_ARGS"]

    return AddTest(name, labels, command, command_args)


def get_group_of_function(node: StatementNode) -> PositionalGroupNode:
    return node.children[-2].children[0]


def flatten_group(node: PositionalGroupNode) -> list[str]:
    trees = (child for child in node.children if isinstance(child, TreeNode))
    return [tree.children[0].content for tree in trees]


@dataclass
class RuntestArgs:
    comparison_mode: str | None
    comparisons: list[tuple[str, str]] | None
    test_command: str
    test_command_arguments: list[str]


def parse_runtest(parameters: list[str]) -> RuntestArgs:
    indexed_params = [
        (idx, param) for (idx, param) in enumerate(parameters) if param.startswith("--")
    ] + [(len(parameters), None)]
    named_parameters = {
        param: parameters[start + 1 : end]
        for ((start, param), (end, _)) in zip_with_next(indexed_params)
    }

    if "--script" in named_parameters:
        script = named_parameters["--script"]
        if len(script) != 1:
            raise ValueError(f"more than one --script: {script}")
        script = script[0]
    else:
        script = None

    if "--files" in named_parameters:
        files_raw = named_parameters["--files"]
        if len(files_raw) % 2 != 0:
            raise ValueError("odd number of files")
        files = list(zip(files_raw[0::2], files_raw[1::2]))
    else:
        files = None

    command_raw = named_parameters["--command"]
    if len(command_raw) != 1:
        raise ValueError(f"more than one --command: {command_raw}")
    command_raw = command_raw[0][1:-1].replace(r"\"", '"')  # remove the quotation marks
    test_full_command = shlex.split(command_raw)
    test_command = test_full_command[0].lstrip("${CMAKE_CURRENT_BINARY_DIR}/")

    return RuntestArgs(script, files, test_command, test_full_command[1:])


@dataclass
class Benchmark:
    module: str
    target: str
    work_dir: str
    command: str
    arguments: list[str]
    comparisons: Comparisons | None

    def reference_files(self: Benchmark, dumux: Path) -> Iterable[Path]:
        if self.comparisons is not None:
            return self.comparisons.reference_files(dumux)
        else:
            return []


@dataclass
class Comparisons:
    mode: str
    references_and_generated: list[tuple[Path, Path]]

    def reference_files(self: Comparisons, dumux: Path) -> Generator[Path]:
        for reference, _ in self.references_and_generated:
            yield dumux / reference


def prepare_benchmark(test: StatementNode) -> Benchmark:
    add_test = parse_add_test(test)
    if add_test.command != "${CMAKE_SOURCE_DIR}/bin/testing/runtest.py":
        raise ValueError(f"unhandled command: {add_test.command}")
    run_test = parse_runtest(add_test.command_args)
    if run_test.comparisons is not None:
        if run_test.comparison_mode is None:
            raise ValueError(f"comparisons without mode: {run_test}")
        else:
            comparisons = Comparisons(
                run_test.comparison_mode,
                list(convert_comparisons(run_test.comparisons)),
            )
    else:
        comparisons = None
    return Benchmark(
        add_test.name,
        add_test.name,
        "src",
        run_test.test_command,
        run_test.test_command_arguments,
        comparisons,
    )


def convert_comparisons(
    comparisons: list[tuple[str, str]],
) -> Generator[tuple[Path, Path]]:
    for reference, generated in comparisons:
        cmake_reference_path = PurePosixPath(reference)
        if str(cmake_reference_path.parts[0]) != "${CMAKE_SOURCE_DIR}":
            raise ValueError(f"unhandled reference location: {reference}")
        reference_path = cmake_reference_path.relative_to("${CMAKE_SOURCE_DIR}")

        cmake_generated_path = PurePosixPath(generated)
        if (
            len(cmake_generated_path.parts) != 2
            or str(cmake_generated_path.parts[0]) != "${CMAKE_CURRENT_BINARY_DIR}"
        ):
            raise ValueError(f"unhandled generated location: {generated}")
        generated_path = cmake_generated_path.relative_to("${CMAKE_CURRENT_BINARY_DIR}")

        yield reference_path, generated_path


def module_cmakelists_txt(module: str) -> str:
    return f"""cmake_minimum_required(VERSION 3.16)
project({module} CXX)

if(NOT (dune-common_DIR OR dune-common_ROOT OR
      "${{CMAKE_PREFIX_PATH}}" MATCHES ".*dune-common.*"))
    string(REPLACE  ${{PROJECT_NAME}} dune-common dune-common_DIR
      ${{PROJECT_BINARY_DIR}})
endif()

#find dune-common and set the module path
find_package(dune-common REQUIRED)
list(APPEND CMAKE_MODULE_PATH ${{dune-common_MODULE_PATH}})

#include the dune macros
include(DuneMacros)

# start a dune project with information from dune.module
dune_project()

dune_enable_all_packages()

add_subdirectory(src)

# finalize the dune project, e.g. generating config.h etc.
finalize_dune_project()
"""


def module_config_h_cmake(module: str) -> str:
    upper_module = module.replace("-", "_").upper()
    return f"""/* begin {module}
   put the definitions for config.h specific to
   your project here. Everything above will be
   overwritten
*/

/* begin private */
/* Name of package */
#define PACKAGE "@DUNE_MOD_NAME@"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "@DUNE_MAINTAINER@"

/* Define to the full name of this package. */
#define PACKAGE_NAME "@DUNE_MOD_NAME@"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "@DUNE_MOD_NAME@ @DUNE_MOD_VERSION@"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "@DUNE_MOD_NAME@"

/* Define to the home page for this package. */
#define PACKAGE_URL "@DUNE_MOD_URL@"

/* Define to the version of this package. */
#define PACKAGE_VERSION "@DUNE_MOD_VERSION@"

/* end private */

/* Define to the version of {module} */
#define {upper_module}_VERSION "@{upper_module}_VERSION@"

/* Define to the major version of {module} */
#define {upper_module}_VERSION_MAJOR @{upper_module}_VERSION_MAJOR@

/* Define to the minor version of {module} */
#define {upper_module}_VERSION_MINOR @{upper_module}_VERSION_MINOR@

/* Define to the revision of {module} */
#define {upper_module}_VERSION_REVISION @{upper_module}_VERSION_REVISION@

/* end {module}
   Everything below here will be overwritten
*/
"""


def module_dune_module(module: str) -> str:
    return f"""################################
# Dune module information file #
################################

# Name of the module
Module: {module}
Version: {DUMUX_VERSION}
Maintainer: noreply@dumux.org
# Required build dependencies
Depends: dumux
# Optional build dependencies
#Suggests:
"""


def module_pc_in(module: str) -> str:
    return f"""prefix=@prefix@
exec_prefix=@exec_prefix@
libdir=@libdir@
includedir=@includedir@
CXX=@CXX@
CC=@CC@
DEPENDENCIES=@REQUIRES@

Name: @PACKAGE_NAME@
Version: @VERSION@
Description: module-name module
URL: http://dune-project.org/
Requires: dumux
Libs: -L${{libdir}}
Cflags: -I${{includedir}}
"""


def add_file_from_string(tar: TarFile, data: str, file: str) -> None:
    encoded = data.encode("utf-8")
    content = BytesIO(encoded)
    info = TarInfo(name=file)
    info.size = len(encoded)
    tar.addfile(info, content)


def package_benchmark(
    benchmark: Benchmark, dumux: Path, benchmark_location: Path
) -> None:
    with tarfile.open(Path(f"{benchmark.module}.tar.xz"), "w:xz") as archive:
        add_file_from_string(
            archive,
            module_cmakelists_txt(benchmark.module),
            f"{benchmark.module}/CMakeLists.txt",
        )
        add_file_from_string(
            archive,
            module_config_h_cmake(benchmark.module),
            f"{benchmark.module}/config.h.cmake",
        )
        add_file_from_string(
            archive,
            module_dune_module(benchmark.module),
            f"{benchmark.module}/dune.module",
        )
        add_file_from_string(
            archive,
            module_pc_in(benchmark.module),
            f"{benchmark.module}/{benchmark.module}.pc.in",
        )

        for file in chain(
            benchmark_location.glob("*.cc"),
            benchmark_location.glob("*.hh"),
            benchmark_location.glob("*.input"),
            [benchmark_location / "CMakeLists.txt"],
        ):
            archive.add(file, f"{benchmark.module}/src/{file.name}")

        for file in benchmark.reference_files(dumux):
            archive.add(file, f"references/{file.name}")

        data = {
            "module": benchmark.module,
            "target": benchmark.target,
            "working-directory": benchmark.work_dir,
            "command": benchmark.command,
            "arguments": benchmark.arguments,
        }
        if benchmark.comparisons is not None:
            data["comparison-mode"] = benchmark.comparisons.mode
            data["comparisons"] = [
                {
                    "generated": generated.name,
                    "reference": reference.name,
                }
                for reference, generated in benchmark.comparisons.references_and_generated
            ]

        add_file_from_string(archive, json.dumps(data, indent=2), "benchmark.json")


def main():
    dumux = Path(f"dumux-{DUMUX_VERSION}")
    for cmake_lists in dumux.glob("examples/*/CMakeLists.txt"):
        tree = parse_file(cmake_lists)
        for test in get_added_tests(tree):
            benchmark = prepare_benchmark(test)
            package_benchmark(benchmark, dumux, cmake_lists.parent)


if __name__ == "__main__":
    main()
