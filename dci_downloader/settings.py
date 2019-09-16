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
        new_settings["topic_name"] = new_settings["topic"]
    if "destination" in new_settings:
        new_settings["destination_folder"] = new_settings["destination"]
    return new_settings


def _get_settings_from_env_variables(env_variables):
    remoteci_id = env_variables.get("DCI_CLIENT_ID")
    settings = {"remoteci_id": remoteci_id.split("/")[1] if remoteci_id else None}
    dci_local_repo = env_variables.get("DCI_LOCAL_REPO")
    if dci_local_repo:
        settings["destination_folder"] = dci_local_repo
    return settings


def get_settings(sys_args, env_variables):
    settings = parse_arguments(sys_args)
    settings.update(_get_settings_from_env_variables(env_variables))
    settings_file_path = settings["settings_file_path"]
    if settings_file_path:
        settings.update(_read_settings_file(settings_file_path))
    return _create_retro_compatible_variables(settings)
