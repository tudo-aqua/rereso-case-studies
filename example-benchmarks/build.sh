#!/usr/bin/env bash

set -euxo pipefail

./download.sh
uv run ./package.py

