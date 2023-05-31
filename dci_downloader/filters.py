#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def _get_patterns(filters):
    variants = filters["variants"]
    archs = filters["archs"]
    with_debug = filters["with_debug"]
    with_source = filters["with_source"]
    patterns = []
    patterns.append(re.compile(r"^metadata"))
    if with_source:
        patterns.append(re.compile(r"^(.*)\/source/tree"))
    archs = archs if archs else [".*"]
    if not variants:
        patterns.append(re.compile(r"^(.*)\/(%s)/os" % "|".join(archs)))
        if with_debug:
            patterns.append(re.compile(r"^(.*)\/(%s)/debug" % "|".join(archs)))
        return patterns
    for variant in variants:
        variant_name = variant["name"]
        variant_with_debug = variant["with_debug"]
        with_iso = variant["with_iso"]
        regex = r"^(%s)\/(%s)/os" % (variant_name, "|".join(archs))
        patterns.append(re.compile(regex))
        if variant_with_debug:
            regex = r"^(%s)\/(%s)/debug" % (variant_name, "|".join(archs))
            patterns.append(re.compile(regex))
        if with_iso:
            regex = r"^(%s)\/(%s)/iso" % (variant_name, "|".join(archs))
            patterns.append(re.compile(regex))
    return patterns


def _match_pattern(string, patterns):
    match = False
    for pattern in patterns:
        if pattern.match(string):
            match = True
            break
    return match


def filter_files_list(topic_info, files_list):
    if topic_info["download_everything"]:
        return files_list
    new_files_list = {"directories": [], "files": [], "symlinks": []}
    patterns = _get_patterns(topic_info)
    for file in files_list["files"]:
        file_path = file["path"]
        if not file["path"]:
            new_files_list["files"].append(file)
        if _match_pattern(file_path, patterns):
            new_files_list["files"].append(file)
    return new_files_list
