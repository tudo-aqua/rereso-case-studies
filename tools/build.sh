#!/usr/bin/env bash

set -euxo pipefail

./download.sh
for f in *.def; do
  singularity build --fakeroot --sandbox --force "${f//def/sif}" "$f"
done

