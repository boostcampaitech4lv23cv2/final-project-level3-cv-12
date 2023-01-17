#!/bin/sh

export CUDA_HOME=/usr/local/cuda-11.2
export PATH=$PATH:$CUDA_HOME/bin/
export LD_LIBRARY_PATH=$CUDA_HOME/lib64/
source ~/.bashrc

nvcc -V