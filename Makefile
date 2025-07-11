# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

SUBDIRS = dumux hpm

.PHONY: all clean all-sub clean-sub

all: case-studies.zip

clean: clean-sub
	rm -f case-studies.zip

case-studies.zip: build-bundle.sh all-sub
	./build-bundle.sh $@

all-sub clean-sub:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir $(@:%-sub=%); done
