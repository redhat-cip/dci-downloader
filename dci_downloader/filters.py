#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def _get_pattern(variants, archs, with_debug):
    variants = variants if variants else [".*"]
    archs = archs if archs else [".*"]
    regex = r"^(%s)\/(%s)/" % ("|".join(variants), "|".join(archs))
    if not with_debug:
        regex += r"os\/"
    return re.compile(regex)


def filter_files_list(files_list, filters):
    if filters["download_everything"]:
        return files_list

    new_files_list = {"directories": [], "files": [], "symlinks": []}

    variants = filters["variants"]
    archs = filters["archs"]
    with_debug = filters["with_debug"]

    pattern = _get_pattern(variants, archs, with_debug)
    for file in files_list["files"]:
        file_path = file["path"]
        if not file["path"]:
            new_files_list["files"].append(file)
        if pattern.match(file_path):
            new_files_list["files"].append(file)

    return new_files_list
