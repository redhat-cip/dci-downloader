#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import yaml

from cli import parse_arguments


def _read_settings_file(settings_file_path):
    with open(settings_file_path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError:
            print("Can't read %s file" % settings_file_path)
            traceback.print_exc()


def _create_retro_compatible_variables(settings):
    new_settings = settings.copy()
    if "topic" in new_settings:
        new_settings["topics_names"] = [new_settings["topic"]]
    if "topics" in new_settings:
        new_settings["topics_names"] = new_settings["topics"]
    return new_settings


def get_settings(sys_args, env_variables):
    settings = {
        "remoteci_id": env_variables["DCI_CLIENT_ID"].split("/")[1],
        "local_storage_folder": env_variables["DCI_LOCAL_REPO"],
    }
    settings.update(parse_arguments(sys_args))
    settings_file_path = settings["settings"]
    if settings_file_path:
        settings.update(_read_settings_file(settings_file_path))
    return _create_retro_compatible_variables(settings)
