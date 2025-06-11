# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

SUBDIRS = native-tools nfc-tool other-log-benchmarks

.PHONY: all clean

all clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir $@; done
