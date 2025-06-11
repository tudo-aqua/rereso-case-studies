<!--
SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md

SPDX-License-Identifier: CC-BY-4.0
-->

# ReReRo Case Studies

This contains all case studies for ReReSo and the scripts to build benchmark and tool bundles from then. The project
contains the following components:

1. The DuMux CI case study in `dumux/ci-tools`, `dumux/example-benchmarks`, and `paper-benchmark`.
2. The DuMux Koch2024a replication case study in `dumux/koch2024a-repro`.
3. The Heat Pump Mining case study in `hpm/native-tools` and `nfc-tool`.
4. The additional log benchmark case study in `hpm/other-log-benchmarks`.

### Running

Building all case study artifacts is done via Makefile. The root Makefile also builds a bundle from the artifacts.

### DuMux CI Benchmarks

We package benchmarks as compressed TAR archives. Each benchmark corresponds to exactly one DuMux-based executable. An
archive contains:

- A metadata file, `benchmark.json`
- A DUNE module for the benchmark that can be built using `dunecontrol`
- Reference outputs in `references`
- Optionally, a `dune.patch` that must be applied to DUNE / DuMux.

We transform all DuMux examples (that double as integration tests) into benchmark packages. This enables running the
tests against different DuMux versions. To further separation, result comparison is delegated to a separate tool. It
becomes possible to, e.g., run a DuMux 3.9.0 example on DuMux 3.8.0 and validate the result using the newer comparator.

We also demonstrate the packaging of a paper artifact as a benchmark. This only requires factoring out necessary
patches and writing the metadata file.

### DuMux CI Tools

We package tools as Singularity containers. Scripts for consuming benchmarks are provided. We create three tools:

- DuMux 3.9.0
- DuMux 3.8.0
- A modified DuMux `runtest.py` that can perform integation test validation in isolation

### Koch2024a Reproduction Package

We package the benchmark as a compressed TAR archive. The archive contains:

- The input control file `flow_one_compartment.input`
- All required inputs, namely `grids/mvn2v2_tortuous_simplified_postpro.dgf`

We package the compiled DuMux tool as a Singularity container and add a script for handling unpacking.

### Heat Pump Mining

We package both the tools from analysis phases one (discretization) and two (selection, learning, evaluation) into
Singularity containers. The second phase tool already natively supports containerization.

Benchmarks are defined via JSON schemas and stored as compressed JSON files. Phase 2 tools are implemented as
benchmark-to-benchmark transformers.

### Additional Logs

We use the transformer in the ReReSo support library to import additional benchmarks into the ReReSo format specified
for the Heat Pump Mining case. These are externally sourced.
