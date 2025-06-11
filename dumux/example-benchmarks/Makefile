# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

.PHONY: all clean

BENCHMARKS = example_1p_rotationsymmetry.tar.xz \
             example_1ptracer.tar.xz \
             example_2p_pointsource_adaptive.tar.xz \
             example_biomineralization.tar.xz \
             example_cahn_hilliard.tar.xz \
             example_cahn_hilliard_parallel.tar.xz \
             example_diffusion.tar.xz \
             example_diffusion_parallel.tar.xz \
             example_embedded_network_1d3d.tar.xz \
             example_ff_liddrivencavity.tar.xz \
             example_ff_liddrivencavity_re1000.tar.xz \
             example_freeflow_channel_navierstokes.tar.xz \
             example_pnm1p_creeping_flow_upscaling.tar.xz \
             example_pnm1p_upscaling.tar.xz \
             example_shallowwaterfriction.tar.xz \

all: $(BENCHMARKS)

clean:
	rm -rf $(BENCHMARKS) dumux-3.9.0 dumux-3.9.0.zip .venv

$(BENCHMARKS)&: dumux-3.9.0
	uv -q run ./package.py

dumux-3.9.0: | dumux-3.9.0.zip
	rm -rf $@
	unzip -qq dumux-3.9.0.zip

dumux-3.9.0.zip:
	wget -q --continue \
	    https://git.iws.uni-stuttgart.de/dumux-repositories/dumux/-/archive/$(@:dumux-%.zip=%)/$@