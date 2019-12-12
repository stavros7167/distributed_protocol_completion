#!/usr/bin/env python

import argparse
import pstats
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Print information from profile files.')
    parser.add_argument('profile',
                        nargs='+',
                        help='File names of profile data')
    args = parser.parse_args()

    for filename in args.profile:
        if not os.path.isfile(filename):
            print "File {} does not exist.".format(filename)
            parser.print_help()
            sys.exit(1)

        stats = pstats.Stats(filename)
        stats.strip_dirs()
        print "*** {} ***\n\n".format(filename)
        stats.print_stats('cegis_solver.*solve')


if __name__ == '__main__':
    main()
