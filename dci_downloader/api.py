#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import shutil

from dciclient.v1.api.context import build_signature_context
from dciclient.v1.api import topic as dci_topic
from dciclient.v1.api import remoteci as dci_remoteci

from http import requests_with_retry


def get_topic(topic_name):
    context = build_signature_context()
    t = dci_topic.list(context, where="name:%s" % topic_name)
    t.raise_for_status()
    topics = t.json()["topics"]
    if len(topics) == 0:
        print("Ensure you have access to topic %s" % topic_name)
        print("Contact your EPM for more information.")
        return
    return topics[0]


def get_components(topic):
    context = build_signature_context()
    return context.session.post(
        "%s/jobs/schedule" % context.dci_cs_api,
        json={"topic_id": topic["id"], "dry_run": True},
    ).json()["components"]


def get_keys(remoteci_id):
    context = build_signature_context()
    remoteci = dci_remoteci.get(context, remoteci_id).json()["remoteci"]
    res = dci_remoteci.refresh_keys(context, id=remoteci_id, etag=remoteci["etag"])

    if res.status_code == 201:
        return res.json()["keys"]


def get_base_url(topic, component):
    return "https://repo.distributed-ci.io/%s/%s/%s" % (
        topic["product_id"],
        topic["id"],
        component["id"],
    )


def get_files_list(base_url, cert, key):
    files_list_url = "%s/dci_files_list.json" % base_url
    r = requests.get(files_list_url, cert=(cert, key))
    r.raise_for_status()
    return r.json()


def download_file(file, cert, key):
    with requests_with_retry().get(file["source"], stream=True, cert=(cert, key)) as r:
        with open(file["destination"], "wb") as f:
            shutil.copyfileobj(r.raw, f)
