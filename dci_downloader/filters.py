#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def _get_patterns(variants, archs, component_type):
    patterns = []
    archs = archs if archs else [".*"]
    if component_type == "puddle_osp":
        patterns.append(re.compile(r"^Packages"))
    if not variants:
        patterns.append(re.compile(r"^(.*)\/(%s)/os" % "|".join(archs)))
    for variant in variants:
        variant_name = variant["name"]
        with_debug = variant["with_debug"]
        regex = r"^(%s)\/(%s)/" % (variant_name, "|".join(archs))
        if not with_debug:
            regex += r"os"
        patterns.append(re.compile(regex))
    return patterns


def _match_pattern(string, patterns):
    match = False
    for pattern in patterns:
        if pattern.match(string):
            match = True
            break
    return match


def filter_files_list(files_list, filters, component_type):
    if filters["download_everything"]:
        return files_list
    new_files_list = {"directories": [], "files": [], "symlinks": []}
    variants = filters["variants"]
    archs = filters["archs"]
    patterns = _get_patterns(variants, archs, component_type)
    for file in files_list["files"]:
        file_path = file["path"]
        if not file["path"]:
            new_files_list["files"].append(file)
        if _match_pattern(file_path, patterns):
            new_files_list["files"].append(file)
    return new_files_list
