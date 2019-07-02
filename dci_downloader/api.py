#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dciclient.v1.api import topic as dci_topic
from dciclient.v1.api import remoteci as dci_remoteci


def get_topic(context, topic_name):
    t = dci_topic.list(context, where="name:%s" % topic_name)
    if t.status_code != 200:
        print("Can't get topic %s" % topic_name)
        print("HTTP error code=%s, message=%s" % (t.status_code, t.text))
        return
    topics = t.json()["topics"]
    if len(topics) == 0:
        print("Ensure you have access to topic %s" % topic_name)
        print("Contact your EPM for more information.")
        return
    return topics[0]


def get_components(context, topic):
    return context.session.post(
        "%s/jobs/schedule" % context.dci_cs_api,
        json={"topic_id": topic["id"], "dry_run": True},
    ).json()["components"]


def get_keys(context, remoteci_id):
    remoteci = dci_remoteci.get(context, remoteci_id).json()["remoteci"]
    res = dci_remoteci.refresh_keys(context, id=remoteci_id, etag=remoteci["etag"])

    if res.status_code == 201:
        return res.json()["keys"]
