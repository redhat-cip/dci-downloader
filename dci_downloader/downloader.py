#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import hashlib
import os
import shutil

import requests


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def _sha256_hexdigest_file(filepath):
    m = hashlib.sha256()
    with open(filepath, mode="rb") as fd:
        for data in fd:
            m.update(data)
    return m.hexdigest()


def _file_exists(file_path):
    return os.path.exists(file_path)


def _file_clean(file_path, sha256):
    return _sha256_hexdigest_file(file_path) == sha256


def get_files_to_download(path, files_list):
    files_to_download = []
    for file in files_list["files"]:
        file_path = os.path.join(path, file["path"], file["name"])
        if os.path.exists(file_path):
            continue
        files_to_download.append(file)
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


def delete_all_symlink_in_path(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                os.unlink(file_path)
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if os.path.islink(folder_path):
                os.unlink(folder_path)


def download_file(url, file_path, cert, key):
    with requests.get(url, stream=True, cert=(cert, key)) as r:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def recreate_symlinks(files_list, local_repo_path):
    for symlink in files_list["symlinks"]:
        link_path = os.path.join(local_repo_path, symlink["path"], symlink["name"])
        os.symlink(symlink["destination"], link_path)


def download(base_url, files_list, local_repo_path, cert, key):
    for file in get_files_to_remove(local_repo_path, files_list):
        print("Remove file %s" % file)
        os.remove(file)

    delete_all_symlink_in_path(local_repo_path)

    files_to_download = get_files_to_download(local_repo_path, files_list)
    nb_files = len(files_to_download)
    for index, file in enumerate(files_to_download):
        file_relative_path = (
            "%s/%s" % (file["path"], file["name"]) if file["path"] else file["name"]
        )
        print("(%d/%d): %s" % (index, nb_files, file_relative_path))
        local_dir = os.path.join(local_repo_path, file["path"])
        mkdir_p(local_dir)
        file_url = "%s/%s" % (base_url, file_relative_path)
        local_file_path = os.path.join(local_dir, file["name"])
        download_file(file_url, local_file_path, cert, key)

    recreate_symlinks(files_list, local_repo_path)
