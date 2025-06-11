#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

shopt -s globstar nullglob

declare -a files

for benchmark in **/rereso-benchmark.yml; do
  files+=( "$benchmark" )
  while IFS= read -r -d '' file; do
    files+=( "$(dirname "$benchmark")/$file" )
  done < <(yq -0 '.benchmarks[].path' "$benchmark")
done

for tool in **/rereso-tool.yml; do
  files+=( "$tool" )
  file="$(yq '.container' "$tool")"
  files+=( "$(dirname "$tool")/$file" )
done

if [ $# -ge 1 ]; then
  exec tar cvf "$1" "${files[@]}"
else
  exec tar cv "${files[@]}"
fi
