#!/usr/bin/env bash

set -euxo pipefail

DUMUX_VERSION='3.9.0'

if [ ! -e "dumux-$DUMUX_VERSION.zip" ]; then
  wget --continue \
       --progress=dot:giga \
       "https://git.iws.uni-stuttgart.de/dumux-repositories/dumux/-/archive/$DUMUX_VERSION/dumux-$DUMUX_VERSION.zip"
fi

if [ ! -e "dumux-$DUMUX_VERSION" ]; then
  unzip "dumux-$DUMUX_VERSION.zip"
fi

cp -v "dumux-$DUMUX_VERSION/bin/testing/runtest.py" .
patch -p1 < runtest.patch
