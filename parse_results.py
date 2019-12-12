#!/usr/bin/env python
import datetime
import sys


def parse_file(filename):
    prev_line = None
    results = {}
    for line in open(filename).read().splitlines():
        if line.startswith('SOLUTION') or line.startswith('NO SOLUTION'):
            benchmark = prev_line
        elif line.startswith('time'):
            dt = datetime.datetime.strptime(line.lstrip('time: '), '%H:%M:%S.%f')
            results[benchmark] = {'time': datetime.timedelta(hours=dt.hour, minutes=dt.minute,
                                                             seconds=dt.second, microseconds=dt.microsecond)}
        elif line.startswith('iterations'):
            results[benchmark]['iterations'] = line.lstrip('iterations: ')
        elif line.startswith('candidate transitions'):
            results[benchmark]['candidate transitions'] = line.lstrip('candidate transitions: ')
        prev_line = line
    return results


def main():
    all_results = {}
    for filename in sys.argv[1:]:
        for benchmark, results in parse_file(filename).items():
            if benchmark in all_results:
                all_results[benchmark]['time'].append(results['time'])
                all_results[benchmark]['iterations'].append(results['iterations'])
                # assert all_results[benchmark]['iterations'] == results['iterations'], '{} {}'.format(benchmark, filename)
                assert all_results[benchmark]['candidate transitions'] == results['candidate transitions']
            else:
                all_results[benchmark] = {'time': [results['time']],
                                          'iterations': [results['iterations']],
                                          'candidate transitions': results['candidate transitions']}

        num_results = len(all_results.values()[0]['time'])
    for benchmark in all_results:
        times = all_results[benchmark]['time']
        assert len(times) == num_results
        assert all(isinstance(time, datetime.timedelta) for time in times)
        all_results[benchmark]['time'] = sum(times, datetime.timedelta()) / len(times)
    for benchmark in sorted(all_results):
        print '{}: {} {} {}'.format(benchmark,
                                    all_results[benchmark]['time'],
                                    all_results[benchmark]['iterations'],
                                    all_results[benchmark]['candidate transitions'])


if __name__ == '__main__':
    main()








