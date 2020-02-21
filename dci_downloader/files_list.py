#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def get_files_to_download(base_url, download_folder, files_list):
    files_to_download = []
    for file in files_list["files"]:
        relative_path = os.path.join(file["path"], file["name"])
        file_path = os.path.join(download_folder, relative_path)
        if os.path.exists(file_path):
            continue
        files_to_download.append(
            {"source": os.path.join(base_url, relative_path), "destination": file_path}
        )
    return files_to_download


def get_files_to_remove(files_list, download_folder):
    files_list_paths = {}
    for file in files_list["files"]:
        file_path = os.path.join(download_folder, file["path"], file["name"])
        files_list_paths[file_path] = file
    files_to_remove = []
    for root, dirs, files in os.walk(download_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                continue
            if (
                file_path not in files_list_paths
                or os.path.getsize(file_path) != files_list_paths[file_path]["size"]
            ):
                files_to_remove.append(file_path)
    return files_to_remove
