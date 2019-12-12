#!/bin/bash

for b in ABP1 ABP2 ABP4 ABPColors1 ABPColors2 ABPColors4 VI VIData consensus_fail consensus_success_no_extra consensus_one_extra_state; do
# for b in VI VIData; do
    for i in `seq 1 1`; do
        echo "runnning $b iteration $i";
        ./run_benchmarks.py $b >| results_new/${b}_$i;
    done;
done
