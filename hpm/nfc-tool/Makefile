# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

.PHONY: all clean

all: nfer_format_compatibility.sif

clean:
	rm -rf nfer_format_compatibility.sif \
           nfer_format_compatibility-0.1.0-py3-none-any.whl \
           nastaran_k77-heat-pump-mining-2120d4230168 \
           nastaran_k77-heat-pump-mining-2120d4230168.zip

nfer_format_compatibility.sif: nfer_format_compatibility.def nfer_format_compatibility-0.1.0-py3-none-any.whl
	singularity -q build $(SINGULARITY_OPTS) --force $@ $<

nfer_format_compatibility-0.1.0-py3-none-any.whl: nastaran_k77-heat-pump-mining-2120d4230168
	cd nastaran_k77-heat-pump-mining-2120d4230168; uv -q build
	cp nastaran_k77-heat-pump-mining-2120d4230168/dist/nfer_format_compatibility-0.1.0-py3-none-any.whl .

nastaran_k77-heat-pump-mining-2120d4230168: | nastaran_k77-heat-pump-mining-2120d4230168.zip
	rm -rf $@
	unzip -qq nastaran_k77-heat-pump-mining-2120d4230168.zip

nastaran_k77-heat-pump-mining-2120d4230168.zip:
	wget -q --continue --trust-server-names --content-disposition \
         https://bitbucket.org/nastaran_k77/heat-pump-mining/get/2120d4230168.zip
