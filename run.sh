#! /bin/bash

# Run unbounded structures
for i in data/unbounded/*.pdb; do pyKVFinder $i --probe_out 12.0 --volume_cutoff 300.0 --depth --hydropathy -O results/${i:5:14}; done

# Run bounded structures
for i in data/bounded/*.pdb; do pyKVFinder $i --probe_out 12.0 --volume_cutoff 300.0 --depth --hydropathy -O results/${i:5:12}; done
