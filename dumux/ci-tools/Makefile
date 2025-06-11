# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

.PHONY: all clean

all: dumux-3.9.0-dune-2.10/dumux-3.9.0-dune-2.10.sif \
	 dumux-3.8.0-dune-2.10/dumux-3.8.0-dune-2.10.sif \
	 runtest/runtest.sif \

clean:
	rm -rf dumux-3.9.0-dune-2.10/dumux-3.9.0-dune-2.10.sif \
           dumux-3.8.0-dune-2.10/dumux-3.8.0-dune-2.10.sif \
           runtest/runtest.sif runtest.py dumux-3.9.0 dumux-3.9.0.zip

dumux-3.9.0-dune-2.10/dumux-3.9.0-dune-2.10.sif: dumux-3.9.0-dune-2.10.def run-rereso-dumux-benchmark
	singularity -q build $(SINGULARITY_OPTS) --force $@ $<

dumux-3.8.0-dune-2.10/dumux-3.8.0-dune-2.10.sif: dumux-3.8.0-dune-2.10.def run-rereso-dumux-benchmark
	singularity -q build $(SINGULARITY_OPTS) --force $@ $<

runtest/runtest.sif: runtest.def runtest.py run-rereso-runtest-benchmark
	singularity -q build $(SINGULARITY_OPTS) --force $@ $<

runtest.py: dumux-3.9.0 runtest.patch
	cp $</bin/testing/$@ .
	patch -s -p1 < $(word 2,$^)

dumux-3.9.0: | dumux-3.9.0.zip
	rm -rf $@
	unzip -qq dumux-3.9.0.zip

dumux-3.9.0.zip:
	wget -q --continue \
         https://git.iws.uni-stuttgart.de/dumux-repositories/dumux/-/archive/$(@:dumux-%.zip=%)/$@
