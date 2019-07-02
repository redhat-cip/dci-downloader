#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os


def _sha256_hexdigest_file(filepath):
    m = hashlib.sha256()
    with open(filepath, mode="rb") as fd:
        for data in fd:
            m.update(data)
    return m.hexdigest()


def _file_clean(file_path, sha256):
    return _sha256_hexdigest_file(file_path) == sha256


def get_files_to_download(base_url, destination_folder, files_list):
    files_to_download = []
    for file in files_list["files"]:
        relative_path = os.path.join(file["path"], file["name"])
        file_path = os.path.join(destination_folder, relative_path)
        if os.path.exists(file_path):
            continue
        files_to_download.append(
            {"source": os.path.join(base_url, relative_path), "destination": file_path}
        )
    return files_to_download


def get_files_to_remove(path, files_list):
    files_list_paths = {}
    for file in files_list["files"]:
        file_path = os.path.join(path, file["path"], file["name"])
        files_list_paths[file_path] = file
    files_to_remove = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                continue
            if file_path not in files_list_paths or not _file_clean(
                file_path, files_list_paths[file_path]["sha256"]
            ):
                files_to_remove.append(file_path)
    return files_to_remove
