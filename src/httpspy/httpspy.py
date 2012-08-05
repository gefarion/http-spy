#!/usr/bin/env/ python

import sys
import argparse
import yaml

from core.http_sniffer import HTTPSniffer
from core.plugins_manager import PluginsManager

# Load plugins
from plugins import *


def parse_arguments():
    parser = argparse.ArgumentParser(description='A very basic http sniffer')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--pcapfile', help='read a tcp stream from a file')
    group.add_argument('--device', help='set the device to sniff')

    parser.add_argument('--filter', help='set the filter (see man tcpdump)',
                      default='')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list-plugins', help='List availables plugins',
                    action='store_true')
    group.add_argument('--help-plugin', help='Show help for a plugin')
    group.add_argument('--plugins', help='File with configured plugins')

    return parser.parse_args()


def list_plugins():
    print "Plugins availables:"
    if len(PluginsManager.list_plugins()) == 0:
        print "No plugins are available."
    else:
        for plugin_name in PluginsManager.list_plugins():
            print "- " + plugin_name
    print "Use '--help-plugin PLUGIN' to see help for a plugin"


def log_with_plugins(http_stream):
    for plugin in PluginsManager.list_initialized_plugins():
        plugin.log_stream(http_stream)


def main(*args):
    # Reading the arguments
    args = parse_arguments()

    # Listing the availables plugins
    if args.list_plugins:
        list_plugins()
        sys.exit(0)

    # Listing the help about a plugin
    if args.help_plugin:
        plugin = PluginsManager.get_plugin(args.help_plugin)
        print plugin.help()
        sys.exit(0)

    # Load the yaml file into a dict
    with open(args.plugins, 'r') as plugin_conf_file:
        plugins_conf = yaml.load(plugin_conf_file)
    plugin_conf_file.closed

    # initializing the plugins
    PluginsManager.init_plugins(plugins_conf)

    # Sniffer initializing
    HTTPSniffer.set_params(callback=log_with_plugins,
                        device=args.device,
                        pcapfile=args.pcapfile,
                        filter=args.filter)

    # Start sniffing
    HTTPSniffer.start()
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
