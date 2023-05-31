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

from argparse import ArgumentParser, ArgumentTypeError
from enum import Enum
import sys as System
import os.path
import shutil
from ruamel.yaml import YAML


class InvalidStateDataException(Exception):
    '''Custom Exception class to be thrown in case there is something wrong with the state file.'''

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

    # prepare things
    yaml = YAML()
    statistics_file_path = parse_arguments()
    statistics_file_path_last = statistics_file_path + '_last'


    # make sure we have a state-file from last run (and if not, abort and don't render any data)
    if os.path.isfile(statistics_file_path_last) is False:
        # create current state file to have it for the next run
        shutil.copy(statistics_file_path, statistics_file_path_last)

        raise InvalidStateDataException('No comparable data, no state file from last run found. Try again.')

    # read yaml file with the raw statistics data
    with open(statistics_file_path, encoding="utf-8") as file_current:
        raw_content_current = file_current.read()
        statistics_current = yaml.load(raw_content_current)
    with open(statistics_file_path_last, encoding="utf-8") as file_last:
        raw_content_last = file_last.read()
        statistics_last = yaml.load(raw_content_last)

    # create current state file to have it for the next run (do it before reading the numbers and
    # throwing Exceptions)
    shutil.copy(statistics_file_path, statistics_file_path_last)

    # gather the relevant current "just in time" values
    zone_count = statistics_current.get('server', {}).get('zone-count', 0)

    # get / compare the counter values (and handle lower values after a service restart)
    query_count = compare_statistics_values(
        statistics_current.get('mod-stats', {}).get('server-operation', {}).get('query', 0),
        statistics_last.get('mod-stats', {}).get('server-operation', {}).get('query', 0)
    )
    query_count_tcp4 = compare_statistics_values(
        statistics_current.get('mod-stats', {}).get('request-protocol', {}).get('tcp4', 0),
        statistics_last.get('mod-stats', {}).get('request-protocol', {}).get('tcp4', 0)
    )
    query_count_tcp6 = compare_statistics_values(
        statistics_current.get('mod-stats', {}).get('request-protocol', {}).get('tcp6', 0),
        statistics_last.get('mod-stats', {}).get('request-protocol', {}).get('tcp6', 0)
    )
    query_count_udp4 = compare_statistics_values(
        statistics_current.get('mod-stats', {}).get('request-protocol', {}).get('udp4', 0),
        statistics_last.get('mod-stats', {}).get('request-protocol', {}).get('udp4', 0)
    )
    query_count_udp6 = compare_statistics_values(
        statistics_current.get('mod-stats', {}).get('request-protocol', {}).get('udp6', 0),
        statistics_last.get('mod-stats', {}).get('request-protocol', {}).get('udp6', 0)
    )

    print(f'OK: Knot doing well, serving {zone_count} zones | zone_count={zone_count} query_counter={query_count}c \
query_counter_tcp4={query_count_tcp4}c query_counter_tcp6={query_count_tcp6}c query_counter_udp4={query_count_udp4}c \
query_counter_udp6={query_count_udp6}c')
    System.exit(State.OK)

def compare_statistics_values(current, last):
    '''Compare current vs. last value and return the difference if it is posived, return 0 if not. \
    This is to overcome the issue of resetted counters upon restart of the Knot DNS service.'''
    difference = current - last
    if difference < 0:
        raise InvalidStateDataException('No comparable data, probably service restarted since last run')
    return difference

def parse_arguments():
    '''Parse arguments before running the script'''

    parser = ArgumentParser(description='Check script to gather Knot DNS server statistics data.')
    parser.add_argument('-f', action='store', dest="statistics_file", help='Path to the statistics dump file.', required=True)
    try:
        args = parser.parse_args()
    except ArgumentTypeError:
        System.exit(State.UNKNOWN)
    return args.statistics_file


if __name__ == "__main__":
    try:
        main()

    except InvalidStateDataException as ex:
        # exit with UNKNOWN state
        print(f'UNKNOWN: Problems with the state-file: {ex}')
        System.exit(State.UNKNOWN)

    # global exception handler to catch *any* Exception, intentionally, and also intentionally disabling the
    # check W0718 from pylint that would complain about the next line of code
    # pylint: disable-next=broad-exception-caught
    except Exception as ex:
        print(f'While executing the script the following error occurred: "{ex}"')
        System.exit(State.WARNING)
