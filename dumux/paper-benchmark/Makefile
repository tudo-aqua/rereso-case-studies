# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

.PHONY: all clean

all: Koch2024a.tar.xz

clean:
	rm -rf Koch2024a.tar.xz Koch2024a Koch2024a-main.zip

Koch2024a.tar.xz: Koch2024a benchmark.json dune.patch
	tar cJf $@ $?

Koch2024a: | Koch2024a-main.zip
	rm -rf $@
	unzip -qq Koch2024a-main.zip
	mv $@-main $@

Koch2024a-main.zip:
	wget -q --continue \
         https://git.iws.uni-stuttgart.de/dumux-pub/Koch2024a/-/archive/main/Koch2024a-main.zip