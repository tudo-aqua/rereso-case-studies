#!/usr/bin/env bash

set -euxo pipefail

if [ ! -e Koch2024a-main.zip ]; then
  wget --continue \
       --progress=dot:giga \
       https://git.iws.uni-stuttgart.de/dumux-pub/Koch2024a/-/archive/main/Koch2024a-main.zip
fi

if [ ! -e Koch2024a-main ]; then
  unzip Koch2024a-main.zip
fi

if [ ! -e Koch2024a ]; then
  cp -r Koch2024a-main Koch2024a
fi

tar cJvf Koch2024a.tar.xz Koch2024a benchmark.json dune.patch

