#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from api import get_files_list, get_base_url, download_file
from stats import check_destination_folder_size
from filters import filter_files_list
from files_list import get_files_to_download, get_files_to_remove
from fs import (
    mkdir_p,
    delete_all_symlink_in_path,
    recreate_symlinks,
    build_destination_folder,
)


def clean_destination_folder(files_list, destination_folder):
    if not os.path.isdir(destination_folder):
        mkdir_p(destination_folder)

    for file in get_files_to_remove(files_list, destination_folder):
        print("Remove file %s" % file)
        os.remove(file)

    delete_all_symlink_in_path(destination_folder)

    for dir in files_list["directories"]:
        dir_path = os.path.join(destination_folder, dir["path"], dir["name"])
        mkdir_p(dir_path)


def download_component(topic, component, arguments, cert, key):
    print("Download component %s" % component["name"])
    base_url = get_base_url(topic, component)
    files_list = get_files_list(base_url, cert, key)
    destination_folder = build_destination_folder(topic, component)
    clean_destination_folder(files_list, destination_folder)
    if topic["name"].startswith("RHEL-8."):
        files_list = filter_files_list(files_list, arguments)
    check_destination_folder_size(files_list, destination_folder)
    files_to_download = get_files_to_download(base_url, destination_folder, files_list)
    nb_files = len(files_to_download)
    for index, file in enumerate(files_to_download):
        print("(%d/%d): %s" % (index, nb_files, file["destination"]))
        download_file(file, cert, key)
    recreate_symlinks(files_list["symlinks"], destination_folder)
