#!/usr/bin/env python

import datetime
import resource
import sys

import cegis
import driver


default_options = driver.DEFAULT_OPTIONS

results = {}

for benchmark in driver.BENCHMARKS:
    if benchmark != sys.argv[1]:
        continue
    if benchmark == 'ABPEmpty':
        continue
    print benchmark

    resources_self_before = resource.getrusage(resource.RUSAGE_SELF)
    resources_children_before = resource.getrusage(resource.RUSAGE_CHILDREN)

    system = driver.BENCHMARK_SPECS[benchmark]['system']()
    options = dict(driver.DEFAULT_OPTIONS)
    options.update(driver.BENCHMARK_SPECS[benchmark]['options'])

    solution, results = cegis.synthesize(system, solver='gurobi', **options)

    resources_self_after = resource.getrusage(resource.RUSAGE_SELF)
    resources_children_after = resource.getrusage(resource.RUSAGE_CHILDREN)

    if solution:
        print "SOLUTION FOUND:"
        for edge in solution:
            print edge
        for a in system.automata:
            if not a.is_environment:
                a.draw_to_file(append=True)
    else:
        print "NO SOLUTION FOUND"

    total_time = (datetime.timedelta(seconds=resources_self_after.ru_utime - resources_self_before.ru_utime) +
                  datetime.timedelta(seconds=resources_children_after.ru_utime - resources_children_before.ru_utime))

    print "time: {}".format(total_time)
    for property in results:
        print '{}: {}'.format(property, results[property])

    results[benchmark] = total_time

print results
