# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

.PHONY: all clean

all: hpm.sif

clean:
	rm -rf hpm.sif heat-pump-mining

hpm.sif: heat-pump-mining
	cd $<; ./gradlew -q singularityImage
	cp $</build/singularity/$@ .

heat-pump-mining:
	rm -rf $@
	git clone https://github.com/tudo-aqua/heat-pump-mining.git
