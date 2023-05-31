#!/usr/bin/env python3
'''Check script for Knot DNS statistics'''

# Script to parse the Knot DNS statistics file and return some counters to
# be able to monitor the smooth operations of a Knot nameserver.
#
# There might be more counters in the statistics file, our goal was not
# to return *all* of them to icinga for charting, just those that we're
# interested in (but might extend this if needed)
#
# (c) Copyright 2023 by Mario Rimann <mario@rimann.org>

from argparse import ArgumentParser
from enum import Enum
import sys as System
from ruamel.yaml import YAML


class State(int, Enum):
    '''Store the possible exit status codes to be used later on.'''

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


CRITICAL_USER_THREADHOLD = 95.00
WARNING_USER_THREADHOLD = 90.00


def main():
    '''Main section of the script'''

    # read yaml file with the raw statistics data
    yaml = YAML()
    statistics_file = parse_arguments()
    statistics_yaml = yaml.load(open(statistics_file))

    # gather the relevant counters
    zone_count = statistics_yaml.get('server', {}).get('zone-count', 0)
    query_count = statistics_yaml.get('mod-stats', {}).get('server-operation', {}).get('query', 0)
    query_count_tcp4 = statistics_yaml.get('mod-stats', {}).get('request-protocol', {}).get('tcp4', 0)
    query_count_tcp6 = statistics_yaml.get('mod-stats', {}).get('request-protocol', {}).get('tcp6', 0)
    query_count_udp4 = statistics_yaml.get('mod-stats', {}).get('request-protocol', {}).get('udp4', 0)
    query_count_udp6 = statistics_yaml.get('mod-stats', {}).get('request-protocol', {}).get('udp6', 0)

    print(f'OK: Knot doing well, serving {zone_count} zones | zone_count={zone_count} query_count={query_count} query_count_tcp4={query_count_tcp4} query_count_tcp6={query_count_tcp6} query_count_udp4={query_count_udp4} query_count_udp6={query_count_udp6}')
    System.exit(State.OK)


def parse_arguments():
    '''Parse arguments before running the script'''

    parser = ArgumentParser(description='Check script to gather Knot DNS server statistics data.')
    parser.add_argument('-f', action='store', dest="statistics_file", help='Path to the statistics dump file.', required=True)
    args = parser.parse_args()
    try:
        args = parser.parse_args()
    except:
        System.exit(State.UNKNOWN)
    return args.statistics_file


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f'While executing the script the following error occurred: "{ex}"')
        System.exit(State.WARNING)
