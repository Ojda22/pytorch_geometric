#!/usr/bin/env bash

CONFIG=${1:-example_node}
# Test for running a single experiment. --repeat means run how many different random seeds.
python main.py --cfg configs/pyg/"${CONFIG}".yaml --repeat 3 # node classification
#python main.py --cfg configs/pyg/example_link.yaml --repeat 3 # link prediction
#python main.py --cfg configs/pyg/example_graph.yaml --repeat 3 # graph classification
