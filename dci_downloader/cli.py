#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from dci_downloader.version import __version__

EXAMPLES = """
examples:
  # download the latest RHEL-8 compose in /tmp/repo
  dci-downloader RHEL-8 /tmp/repo

  # download specific arch
  dci-downloader RHEL-8 /tmp/repo --arch ppc64le

  # download explicit variants
  dci-downloader RHEL-8 /tmp/repo --variant AppStream --variant BaseOS

  # load options from yaml settings file
  dci-downloader --settings settings.yml
"""

COPYRIGHT = """
copyright:
  Copyright © 2019 Red Hat.
  Licensed under the Apache License, Version 2.0
"""


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(
        usage="dci-downloader TOPIC DEST [OPTIONS]",
        description="Download the latest RHEL compose easily:\n * source your credentials file\n * specify the topic name and the destination folder",
        epilog=EXAMPLES + COPYRIGHT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "name",
        metavar="TOPIC",
        nargs="?",
        help="topic name (i.e. RHEL-7.8, RHEL-8.1, etc...)",
    )
    parser.add_argument(
        "download_folder", metavar="DEST", nargs="?", help="destination folder."
    )
    parser.add_argument(
        "--components",
        nargs='+',
        metavar="COMPONENTS",
        dest="components",
        default=[],
        help="download specific components by name or id (default: all)",
    )
    parser.add_argument(
        "--arch",
        action="append",
        metavar="ARCH",
        dest="archs",
        default=[],
        help="download a specific architecture (default: x86_64)",
    )
    parser.add_argument(
        "--variant",
        action="append",
        metavar="VARIANT",
        dest="variants",
        default=[],
        help="download a specific variant (default: all variants)",
    )
    parser.add_argument(
        "--debug", help="download debug RPMs", dest="with_debug", action="store_true"
    )
    parser.add_argument(
        "--all",
        help="download all archs, all variants with debugs rpms",
        dest="download_everything",
        action="store_true",
    )
    parser.add_argument(
        "--settings",
        dest="settings_file_path",
        metavar="FILE_PATH",
        help="settings file to overwrite cli parameters",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parsed_arguments = parser.parse_args(arguments)
    if not parsed_arguments.archs:
        parsed_arguments.archs = ["x86_64"]
    parsed_arguments.archs = list(set(parsed_arguments.archs))

    if parsed_arguments.settings_file_path is None:
        topic_name = parsed_arguments.name
        download_folder = parsed_arguments.download_folder
        if topic_name is None or download_folder is None:
            print(
                "TOPIC and DEST arguments or --settings FILE_PATH are mutually exclusive"
            )
            print("Try 'dci-downloader --help' for more information.")
            sys.exit(2)
    parsed_arguments.variants = [
        {"name": v, "with_debug": parsed_arguments.with_debug}
        for v in parsed_arguments.variants
    ]
    return vars(parsed_arguments)
