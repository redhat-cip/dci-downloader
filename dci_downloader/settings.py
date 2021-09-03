#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import traceback
import yaml
import sys

from collections import defaultdict

from dci_downloader.cli import parse_arguments
from dci_downloader.containers import has_command


def _read_settings_files(settings_files_paths=[]):
    settings = {}
    for settings_file_path in settings_files_paths:
        with open(settings_file_path, "r") as stream:
            try:
                settings.update(yaml.safe_load(stream))
            except yaml.YAMLError:
                print("Can't read %s file" % settings_file_path)
                traceback.print_exc()
    return settings


def _clean_topic(topic):
    name = topic.get("topic", topic.get("name"))
    component_id = topic.get("component_id")
    components = topic.get("components", [])
    archs = topic.get("archs", ["x86_64"])
    variants = topic.get("variants", [])
    variants = [
        v if type(v) is dict else {"name": v, "with_debug": False, "with_iso": False}
        for v in variants
    ]
    filters = topic.get("filters", [])
    return {
        "name": name,
        "components": components,
        "archs": archs,
        "variants": variants,
        "download_everything": topic.get("download_everything", False),
        "download_folder": topic["download_folder"],
        "dci_key_file": topic["dci_key_file"],
        "dci_cert_file": topic["dci_cert_file"],
        "registry": topic["registry"],
        "component_id": component_id,
        "with_debug": topic.get("with_debug", False),
        "filters": filters,
    }


def _clean_settings(settings):
    dci_home_path = _get_dci_downloader_home_folder(settings["env_variables"])
    key = settings.get("dci_key_file", os.path.join(dci_home_path, "dci.key"))
    crt = settings.get("dci_cert_file", os.path.join(dci_home_path, "dci.crt"))
    new_settings = {
        "version": int(settings.get("version", "1")),
        "env_variables": settings["env_variables"],
        "dci_key_file": key,
        "dci_cert_file": crt,
    }
    new_topics = []
    for topic in settings["topics"]:
        topic["download_folder"] = settings["download_folder"]
        topic["dci_key_file"] = key
        topic["dci_cert_file"] = crt
        topic["registry"] = settings["registry"]
        new_topics.append(_clean_topic(topic))
    new_settings["topics"] = sorted(new_topics, key=lambda k: k["name"])
    return new_settings


def _keep_backward_compatibility(settings):
    if "local_repo" in settings:
        settings["download_folder"] = settings["local_repo"]
    if "topic" in settings:
        settings["topics"] = [settings.copy()]
    if "jobs" in settings:
        settings["topics"] = settings["jobs"]
    if "download_key_file" in settings:
        settings["dci_key_file"] = settings["download_key_file"]
    if "download_crt_file" in settings:
        settings["dci_cert_file"] = settings["download_crt_file"]
    settings["download_folder"] = settings.get("download_folder")
    settings["registry"] = settings.get("registry")
    settings["topics"] = settings.get("topics", [])
    return settings


def _get_dci_downloader_home_folder(env_variables):
    DEFAULT_XDG_DATA_HOME = os.path.join(os.path.expanduser("~"), ".local", "share")
    data_home_path = env_variables.get("XDG_DATA_HOME", DEFAULT_XDG_DATA_HOME)
    return os.path.join(data_home_path, "dci-downloader")


def _remove_none_values(d):
    return {k: v for k, v in d.items() if v is not None}


def _merge_settings(settings):
    topics_by_name = defaultdict(dict)
    for setting in settings:
        for topic in setting.get("topics", []):
            k = "name" if "name" in topic else "topic"
            topics_by_name[topic[k]].update(topic)
    s = {}
    s.update(settings[0])
    s.update(settings[1])
    s.update(settings[2])
    s["topics"] = list(topics_by_name.values())
    return s


def get_settings(sys_args, env_variables={}):
    settings_from_env_variables = {
        "env_variables": env_variables,
        "dci_key_file": env_variables.get("DCI_KEY_FILE"),
        "dci_cert_file": env_variables.get("DCI_CERT_FILE"),
        "download_folder": env_variables.get("DCI_LOCAL_REPO"),
        "registry": env_variables.get("DCI_REGISTRY"),
    }

    cli_arguments = parse_arguments(sys_args)
    settings_from_cli = {
        "download_folder": cli_arguments["download_folder"],
        "registry": cli_arguments["registry"],
        "topics": [],
    }
    topic_name = cli_arguments["name"]
    if topic_name:
        settings_from_cli["topics"].append(
            {
                "download_everything": cli_arguments["download_everything"],
                "variants": cli_arguments["variants"],
                "with_debug": cli_arguments["with_debug"],
                "name": topic_name,
                "with_iso": cli_arguments["with_iso"],
                "archs": cli_arguments["archs"],
                "filters": cli_arguments["filters"],
                "component_id": cli_arguments["component_id"],
            }
        )

    settings_from_files = {"download_folder": None, "registry": None, "topics": []}
    settings_files_paths = cli_arguments["settings_files_paths"]
    if settings_files_paths:
        settings_from_files.update(
            _keep_backward_compatibility(_read_settings_files(settings_files_paths))
        )

    settings = _merge_settings(
        [
            settings_from_files,
            _remove_none_values(settings_from_env_variables),
            _remove_none_values(settings_from_cli),
        ]
    )

    return _clean_settings(settings)


def _variants_are_invalid(topic):
    topic_variants = {
        "RHEL-7": [
            "Client-optional",
            "Client",
            "ComputeNode-optional",
            "ComputeNode",
            "Server-NFV",
            "Server-RT",
            "Server-SAP",
            "Server-SAPHANA",
            "Server-optional",
            "Server",
            "Workstation-optional",
            "Workstation",
        ],
        "RHEL-8": [
            "AppStream",
            "BaseOS",
            "CRB",
            "HighAvailability",
            "NFV",
            "RT",
            "ResilientStorage",
            "SAP",
            "SAPHANA",
        ],
        "RHEL-9": [
            "AppStream",
            "BaseOS",
            "CRB",
            "HighAvailability",
            "NFV",
            "RT",
            "ResilientStorage",
            "SAP",
            "SAPHANA",
        ],
    }
    invalid = False
    for topic_name, variants in topic_variants.items():
        current_topic_name = topic["name"]
        current_variants = [v["name"] for v in topic["variants"]]
        variants_not_allowed = set(current_variants) - set(variants + ["metadata"])
        if current_topic_name.startswith(topic_name) and variants_not_allowed:
            invalid = True
            print(
                "Variants %s for the %s topic are not valid"
                % (", ".join(variants_not_allowed), current_topic_name)
            )
            print(
                "The authorized variants for %s are %s."
                % (current_topic_name, ", ".join(variants))
            )
            break
    return invalid


def _arches_are_invalid(topic):
    topic_archs = {
        "RHEL-7": ["ppc64", "ppc64le", "s390x", "x86_64"],
        "RHEL-8": ["aarch64", "ppc64le", "s390x", "x86_64"],
        "RHEL-9": ["aarch64", "ppc64le", "s390x", "x86_64"],
    }
    invalid = False
    current_topic_name = topic["name"]
    for topic_name, archs in topic_archs.items():
        archs_not_allowed = set(topic["archs"]) - set(archs)
        if current_topic_name.startswith(topic_name) and archs_not_allowed:
            invalid = True
            print(
                "Arches %s for the %s topic are not valid"
                % (", ".join(archs_not_allowed), current_topic_name)
            )
            print(
                "The authorized archs for %s are %s."
                % (current_topic_name, ", ".join(archs))
            )
            break
    return invalid


def exit_if_settings_invalid(settings):
    has_error = False
    for env_variable in ["DCI_CLIENT_ID", "DCI_API_SECRET", "DCI_CS_URL"]:
        if env_variable not in settings["env_variables"]:
            has_error = True
            print("Environment variable %s not set" % env_variable)

    topics = settings["topics"]
    if not topics:
        has_error = True
        print("You need to specify at least one topic")

    for topic in topics:
        if topic.get("download_folder") is None:
            has_error = True
            print("The destination folder for the download is not specified.")

        if topic.get("registry") and not has_command("skopeo sync --help"):
            has_error = True
            print(
                "You specified a registry to mirror container images "
                "but `skopeo sync [...]` is not available on your system. "
                "Please ensure that skopeo >= 0.1.41 is installed."
            )

    for topic in topics:
        if _variants_are_invalid(topic):
            has_error = True
        if _arches_are_invalid(topic):
            has_error = True

    if has_error:
        sys.exit(1)
