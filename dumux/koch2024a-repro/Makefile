# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

.PHONY: all clean

all: Koch2024a.sif flow_one_compartment.tar.xz

clean:
	rm -rf Koch2024a.sif koch2024a.tar \
           flow_one_compartment.tar.xz Koch2024a-main Koch2024a-main.zip

Koch2024a.sif: Koch2024a.def koch2024a.tar unpack-and-run
	singularity -q build $(SINGULARITY_OPTS) --force $@ $<

koch2024a.tar: Koch2024a-main
	docker build -q -t $(@:%.tar=%) $</docker
	docker save $(@:%.tar=%) -o $@

flow_one_compartment.tar.xz: Koch2024a-main
	cd $</app; \
    tar cJf ../../flow_one_compartment.tar.xz \
            flow_one_compartment.input grids/mvn2v2_tortuous_simplified_postpro.dgf

Koch2024a-main: | Koch2024a-main.zip
	rm -rf $@
	unzip -qq Koch2024a-main.zip

Koch2024a-main.zip:
	wget -q --continue \
         https://git.iws.uni-stuttgart.de/dumux-pub/Koch2024a/-/archive/main/$@