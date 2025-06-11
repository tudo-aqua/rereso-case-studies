# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

SUBDIRS = dumux hpm

.PHONY: all clean all-sub clean-sub

all: bundle.tar.zst

clean: clean-sub
	rm -f bundle.zip

bundle.tar.zst: build-bundle.sh all-sub
	./build-bundle.sh | zstd > bundle.tar.zst

all-sub clean-sub:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir $(@:%-sub=%); done
