#!/usr/bin/env python
# -*- coding: utf-8 -*-
from simulationfiles import nodes_config
from simulationfiles import ticks_config
from simulationfiles import network_config
import sys
import argparse
import simulation
import config
import os

sys.tracebacklimit = None


def run():
    nodes_config.create(unkown_arguments=True)

    ticks_config.create(unkown_arguments=True)

    network_config.create(unkown_arguments=True)

    simulation.run(unkown_arguments=True)

commands = {
    'nodes':        nodes_config.create,
    'network':      network_config.create,
    'ticks':        ticks_config.create,
    'simulate':     simulation.run,
    'run':          run,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Simcoin a cryptocurrency simulator.',
        usage='''<command> [<args>]

        The commands are:
        nodes       creates the {} for a simulation
        network     creates the {} for a simulation
        ticks       creates the {} for a simulation
        simulate    executes a simulation based on the {}, {} and {}
        run         runs all above commands
        '''.format(
            config.nodes_json_file_name, config.network_csv_file_name, config.ticks_csv_file_name,
            config.nodes_json_file_name, config.network_csv_file_name, config.ticks_csv_file_name,
        ))

    parser.add_argument('command', help='Subcommand to run')
    # parse_args defaults to [1:] for args, but you need to
    # exclude the rest of the args too, or validation will fail
    args = parser.parse_args(sys.argv[1:2])
    if args.command not in commands:
        print('Unrecognized command')
        parser.print_help()
        exit(1)
    # use dispatch pattern to invoke method with same name

    if not os.path.exists(config.data_dir):
        os.makedirs(config.data_dir)

    commands[args.command]()
