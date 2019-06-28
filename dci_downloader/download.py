#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ansible_runner
import json
import os
import sys

from cli import parse_arguments

from dciclient.v1.api.context import build_signature_context
from dciclient.v1.api import remoteci as dci_remoteci
from dciclient.v1.api import topic as dci_topic


def verify_env_variables_needed_are_setted():
    expected_env_variables = ["DCI_CLIENT_ID", "DCI_API_SECRET", "DCI_CS_URL"]
    for env_variable in expected_env_variables:
        if env_variable not in os.environ:
            print("Ensure %s variables are set" % ",".join(expected_env_variables))
            sys.exit(1)


def extend_dci_topic_with_control_server_info(topic):
    context = build_signature_context()
    topic_name = topic["name"]
    t = dci_topic.list(context, where="name:%s" % topic_name)
    if t.status_code != 200:
        print("Can't get topic %s" % topic_name)
        print("HTTP error code=%s, message=%s" % (t.status_code, t.text))
    topics = t.json()["topics"]
    if len(topics) == 0:
        print("Ensure you have access to topic %s" % topic_name)
        print("Contact your EPM for more information.")
        return
    topic.update(topics[0])
    return topic


def get_components(topic):
    context = build_signature_context()
    return context.session.post(
        "%s/jobs/schedule" % context.dci_cs_api,
        json={"topic_id": topic["id"], "dry_run": True},
    ).json()["components"]


def main():
    verify_env_variables_needed_are_setted()
    remoteci_id = os.getenv("DCI_CLIENT_ID").split("/")[1]
    arguments = parse_arguments(sys.argv[1:])
    context = build_signature_context()
    has_error = False
    for topic in arguments["topics"].values():
        topic = extend_dci_topic_with_control_server_info(topic)
        if topic is None:
            has_error = True
            continue
        extravars = {
            "local_repo": "/var/lib/dci",
            "remoteci_id": remoteci_id,
            "product": topic["product_id"],
            "topic_id": topic["id"],
            "topic_name": topic["name"],
            "components": get_components(topic),
        }
        print(json.dumps(extravars, indent=4, sort_keys=True))
        r = ansible_runner.run(
            private_data_dir="/usr/share/dci-downloader",
            playbook="download-components.yml",
            extravars=extravars,
        )
        if r.rc != 0:
            print("Error! Download components has failed.")
            print("%s: %s" % (r.status, r.rc))
            has_error = True
    return_code = 1 if has_error else 0
    sys.exit(return_code)


if __name__ == "__main__":
    main()
