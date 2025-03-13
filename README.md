# DuMux ReReRo Case Study

This case study demonstrates the application of the ReReSo approach to DuMux. To increase the reusability of research
software and benchmarks, the ReReSp approach aims to separate the two to facilitate recombination.

This project contains three modules, described below:

### Benchmark Layout

We package benchmarks as compressed TAR archives. Each benchmark corresponds to exactly one DuMux-based executable. An
archive contains:

- A metadata file, `benchmark.json`
- A DUNE module for the benchmark that can be built using `dunecontrol`
- Reference outputs in `references`
- Optionally, a `dune.patch` that must be applied to DUNE / DuMux.

### Tool Layout

We package tools as Singularity containers. Scripts for consuming benchmarks are provided.

### Case Studies

This repository contains three case studies: tool packaging, intergration test packaging, and paper artifact packaging.
We create three tools:

- DuMux 3.9.0
- DuMux 3.8.0
- A modified DuMux `runtest.py` that can perform integation test validation in isolation

We transform all DuMux examples (that double as integration tests) into benchmark packages. This enables running the
tests against different DuMux versions. To further separation, result comparison is delegated to a separate tool. It
becomes possible to, e.g., run a DuMux 3.9.0 example on DuMux 3.8.0 and validate the result using the newer comparator.

Finally, we demonstrate the packaging of a paper artifact as a benchmark. This only requires factoring out necessary
patches and writing the metadata file.
 
