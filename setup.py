#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import os
import setuptools

# dcibuild can be loaded only when doing the sdist sub-command because
# dci-packaging is extracted at the same level. When doing the other
# sub-commands like build, we extract the version from version.py.
try:
    from dcibuild import sdist, get_version

    sdist.dci_mod = "dci_downloader"
except:
    sdist = None

    def get_version():
        from dci_downloader import version

        return version.__version__


root_dir = os.path.dirname(os.path.abspath(__file__))
readme = open(os.path.join(root_dir, "README.md"), "rb").read().decode("utf-8")
requirements = open(os.path.join(root_dir, "requirements.txt")).read()
install_requires = [r.split("==")[0] for r in requirements.split("\n")]

setuptools.setup(
    name="dci-downloader",
    version=get_version(),
    packages=["dci_downloader"],
    author="Distributed CI team",
    author_email="distributed-ci@redhat.com",
    description="DCI downloader module",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    extras_require={':python_version == "2.7"': ["futures"]},
    url="https://github.com/redhat-cip/dci-downloader",
    license="Apache v2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["dci-downloader = dci_downloader.main:main"]},
    cmdclass={
        "sdist": sdist,
    },
)
