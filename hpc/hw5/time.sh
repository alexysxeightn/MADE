#!/bin/bash

chmod +x automata.py

for i in $(seq 1 $1)
do
    mpirun --allow-run-as-root -n $i automata.py --num-epochs 1000 --size 720 --periodic
done