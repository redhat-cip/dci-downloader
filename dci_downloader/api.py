#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import sys
import time

from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from threading import local

from dci_downloader.fs import create_parent_dir
from dciclient.v1.api.context import build_signature_context, DciSignatureAuth
from dciclient.v1.api import component as dci_component
from dciclient.v1.api import topic as dci_topic
from dciclient.v1.api import remoteci as dci_remoteci

FIVE_SECONDS = 5
TEN_SECONDS = 10
# We'll allow 5 seconds to connect & 10 seconds to get an answer
REQUESTS_TIMEOUT = (FIVE_SECONDS, TEN_SECONDS)


def _check_url_is_accessible(url):
    try:
        requests.get(url, timeout=REQUESTS_TIMEOUT)
    except requests.exceptions.Timeout:
        print("Timeout. dci-downloader cannot access %s url." % url)
        if os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY"):
            print("You configured a proxy. Check your proxy information.")
        print("Exiting...")
        sys.exit(1)


def check_repo_is_accessible(topic_info):
    _check_url_is_accessible(topic_info["repo_url"])


def check_api_is_accessible(topic_info):
    _check_url_is_accessible(topic_info["cs_url"])


def get_topic(topic_name):
    context = build_signature_context()
    t = dci_topic.list(context, where="name:%s,state:active" % topic_name)
    t.raise_for_status()
    topics = t.json()["topics"]
    if len(topics) == 0:
        print("Ensure you have access to topic %s" % topic_name)
        print("Contact your EPM for more information.")
        return
    return topics[0]


def get_topic_by_id(topic_id):
    context = build_signature_context()
    c = dci_topic.get(context, topic_id)
    topic = c.json()["topic"]
    if len(topic) == 0:
        print("Ensure that topic %s exists or that you have access" % topic_id)
        print("Contact your EPM for more information.")
        return
    return topic


def get_component_by_id(component_id):
    context = build_signature_context()
    c = dci_component.get(context, component_id)
    component = c.json()["component"]
    if len(component) == 0:
        print("Ensure that component %s exists or that you have access" % component_id)
        print("Contact your EPM for more information.")
        return
    return component


def get_components_per_topic(
    topic_id, sort="-created_at", limit=100, offset=0, where=""
):
    response = dci_topic.list_components(
        context=build_signature_context(),
        id=topic_id,
        sort=sort,
        limit=limit,
        offset=offset,
        where=where,
    ).json()
    return response["components"]


def get_components(topic, filters=[]):
    returned_components = []
    tag_per_type = {filter["type"]: filter["tag"] for filter in filters}
    for component_type in topic["component_types"]:
        component_type = component_type.lower()
        where = "type:%s,state:active" % component_type
        if component_type in tag_per_type:
            where += ",tags:%s" % tag_per_type[component_type]
        components = get_components_per_topic(
            topic_id=topic["id"],
            sort="-created_at",
            limit=1,
            offset=0,
            where=where,
        )
        returned_components.extend(components)
    return returned_components


def get_keys(remoteci_id):
    context = build_signature_context()
    r = dci_remoteci.get(context, remoteci_id)
    r.raise_for_status()
    remoteci = r.json()["remoteci"]
    r = dci_remoteci.refresh_keys(context, id=remoteci_id, etag=remoteci["etag"])
    r.raise_for_status()
    return r.json()["keys"]


def cert_is_valid(cert_file):
    try:
        context = build_signature_context()
        with open(cert_file, "r") as f:
            cert = f.read()
            uri = "%s/certs/check" % context.dci_cs_api
            r = context.session.post(uri, json={"cert": cert})
            return r.status_code == 204
    except Exception:
        return False


def is_component_on_s3(remoteci_context):
    try:
        r = remoteci_context.head("dci_files_list.json")
        r.raise_for_status()
        print("Getting component files from API+S3")
        return True
    except Exception:
        print("Getting component files from legacy repository")
        return False


def build_s3_context(component_id, cs_url, client_id, api_secret):
    class S3Context(object):
        """
        S3Context builds a request Session() object configured to download
        files from S3 through a redirection from DCI API.
        """

        def __init__(self, base_url, client_id, api_secret):
            self.threadlocal = local()
            self.session_auth = DciSignatureAuth(client_id, api_secret)
            self.base_url = base_url

        @property
        def session(self):
            """
            Each thread must have its own `requests.Session()` instance.
            `session` is a property looking for `session` object in a
            thread-local context.
            """
            if not hasattr(self.threadlocal, "session"):
                session = requests.Session()
                session.auth = self.session_auth
                session.timeout = REQUESTS_TIMEOUT
                session.stream = True
                self.threadlocal.session = session
            return self.threadlocal.session

        def get(self, relpath):
            return self.session.get("%s/%s" % (self.base_url, relpath.lstrip("/")))

        def head(self, relpath):
            # allow_redirects must be set to True to get the final HTTP status
            return self.session.head(
                "%s/%s" % (self.base_url, relpath.lstrip("/")), allow_redirects=True
            )

    base_url = "%s/api/v1/components/%s/files" % (cs_url, component_id)
    return S3Context(base_url, client_id, api_secret)


def build_repo_context(product_id, topic_id, component_id, repo_url, cert, key):
    class RepoContext(object):
        """
        RepoContext builds a request Session() object configured to download
        files from `repo.distributed-ci.io` authenticated by a TLS client
        certificate and private key.
        """

        def __init__(self, base_url, cert, key):
            self.threadlocal = local()
            self.session_cert = (cert, key)
            self.base_url = base_url

        @property
        def session(self):
            """
            Each thread must have its own `requests.Session()` instance.
            `session` is a property looking for `session` object in a
            thread-local context.
            """
            if not hasattr(self.threadlocal, "session"):
                session = requests.Session()
                session.cert = self.session_cert
                session.timeout = REQUESTS_TIMEOUT
                session.stream = True
                self.threadlocal.session = session
            return self.threadlocal.session

        def get(self, relpath):
            return self.session.get("%s/%s" % (self.base_url, relpath.lstrip("/")))

        def head(self, relpath):
            # allow_redirects must be set to True to get the final HTTP status
            return self.session.head(
                "%s/%s" % (self.base_url, relpath.lstrip("/")), allow_redirects=True
            )

    base_url = "%s/%s/%s/%s" % (repo_url, product_id, topic_id, component_id)
    return RepoContext(base_url, cert, key)


def retry(tries=3, delay=2, multiplier=2):
    def decorated_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            _tries = tries
            _delay = delay
            while _tries:
                try:
                    return f(*args, **kwargs)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print("%s, retrying in %d seconds..." % (str(e), _delay))
                    time.sleep(_delay)
                    _tries -= 1
                    if not _tries:
                        raise
                    _delay *= multiplier
            return f(*args, **kwargs)

        return f_retry

    return decorated_retry


@retry()
def get_files_list(context):
    print("Download DCI file list, it may take a few seconds")
    r = context.get("dci_files_list.json")
    r.raise_for_status()
    return r.json()


def get_and_save_image_list(context, download_folder):
    try:
        images_list_file_name = "images_list.yaml"
        r = context.get(images_list_file_name)
        r.raise_for_status()
        images_list = r.content
        with open(os.path.join(download_folder, images_list_file_name), "wb") as f:
            f.write(images_list)
        return images_list
    except Exception:
        return None


@retry()
def download_file(context, file, i, nb_files):
    start_time = time.monotonic()
    destination = file["destination"]
    print("(%d/%d): < Getting %s" % (i + 1, nb_files, destination))
    create_parent_dir(destination)
    r = context.get(file["source"])
    r.raise_for_status()
    with open(destination, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
    print(
        "(%d/%d): > Done %s - %.2f KB/s"
        % (
            i + 1,
            nb_files,
            destination,
            file["size"] / (time.monotonic() - start_time) / 1024,
        )
    )
    return file


def download_files(context, files):
    nb_files = len(files)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for file in executor.map(
            download_file,
            *zip(*[(context, file, i, nb_files) for i, file in enumerate(files)])
        ):
            pass
