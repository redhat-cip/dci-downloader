from dci_downloader.filters import filter_files_list
from dci_downloader.settings import get_settings


def test_default_filter_files_list():
    dci_files_list = {
        "directories": [],
        "files": [
            {
                "path": "",
                "sha256": "954719cab91afac5bc142656afff86e6d8e87570b035cbce65dbbb84892a40d3",
                "name": ".composeinfo",
                "size": 14496,
            },
            {
                "path": "AppStream/x86_64/debug/tree/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.x86_64.rpm",
                "size": 45052,
            },
            {
                "path": "AppStream/x86_64/os/Packages",
                "sha256": "8fe293470f677bfc6eb04204c47b5e1a0e5d15431ef7ed9dbb269aaea386ed9f",
                "name": "PackageKit-command-not-found-1.1.12-2.el8.x86_64.rpm",
                "size": 28616,
            },
            {
                "path": "BaseOS/x86_64/os/Packages",
                "sha256": "7949b18b6d359b435686f2f5781928675ec8b2872b96f0abf6ba10747f794694",
                "name": "avahi-libs-0.7-19.el8.i686.rpm",
                "size": 68920,
            },
            {
                "path": "AppStream/s390x/os/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.s390x.rpm",
                "size": 29562,
            },
            {
                "path": "AppStream/x86_64/os",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": ".treeinfo",
                "size": 29562,
            },
        ],
        "symlinks": [],
    }
    settings = get_settings(sys_args=["RHEL-8", "/tmp"])["topics"][0]
    expected_files_list = {
        "directories": [],
        "files": [
            {
                "path": "",
                "sha256": "954719cab91afac5bc142656afff86e6d8e87570b035cbce65dbbb84892a40d3",
                "name": ".composeinfo",
                "size": 14496,
            },
            {
                "path": "AppStream/x86_64/os/Packages",
                "sha256": "8fe293470f677bfc6eb04204c47b5e1a0e5d15431ef7ed9dbb269aaea386ed9f",
                "name": "PackageKit-command-not-found-1.1.12-2.el8.x86_64.rpm",
                "size": 28616,
            },
            {
                "path": "BaseOS/x86_64/os/Packages",
                "sha256": "7949b18b6d359b435686f2f5781928675ec8b2872b96f0abf6ba10747f794694",
                "name": "avahi-libs-0.7-19.el8.i686.rpm",
                "size": 68920,
            },
            {
                "path": "AppStream/x86_64/os",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": ".treeinfo",
                "size": 29562,
            },
        ],
        "symlinks": [],
    }
    assert filter_files_list(dci_files_list, settings) == expected_files_list


def test_filter_files_list_with_debug():
    dci_files_list = {
        "directories": [],
        "files": [
            {
                "path": "AppStream/x86_64/debug/tree/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.x86_64.rpm",
                "size": 45052,
            },
            {
                "path": "AppStream/x86_64/os/Packages",
                "sha256": "8fe293470f677bfc6eb04204c47b5e1a0e5d15431ef7ed9dbb269aaea386ed9f",
                "name": "PackageKit-command-not-found-1.1.12-2.el8.x86_64.rpm",
                "size": 28616,
            },
        ],
        "symlinks": [],
    }
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp", "--variant", "AppStream", "--debug"]
    )["topics"][0]
    expected_files_list = {
        "directories": [],
        "files": [
            {
                "path": "AppStream/x86_64/debug/tree/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.x86_64.rpm",
                "size": 45052,
            },
            {
                "path": "AppStream/x86_64/os/Packages",
                "sha256": "8fe293470f677bfc6eb04204c47b5e1a0e5d15431ef7ed9dbb269aaea386ed9f",
                "name": "PackageKit-command-not-found-1.1.12-2.el8.x86_64.rpm",
                "size": 28616,
            },
        ],
        "symlinks": [],
    }
    assert filter_files_list(dci_files_list, settings) == expected_files_list


def test_non_existing_variants_are_ignored():
    dci_files_list = {
        "directories": [],
        "files": [
            {
                "path": "",
                "sha256": "954719cab91afac5bc142656afff86e6d8e87570b035cbce65dbbb84892a40d3",
                "name": ".composeinfo",
                "size": 14496,
            },
            {
                "path": "AppStream/x86_64/debug/tree/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.x86_64.rpm",
                "size": 45052,
            },
            {
                "path": "AppStream/x86_64/os/Packages",
                "sha256": "8fe293470f677bfc6eb04204c47b5e1a0e5d15431ef7ed9dbb269aaea386ed9f",
                "name": "PackageKit-command-not-found-1.1.12-2.el8.x86_64.rpm",
                "size": 28616,
            },
            {
                "path": "BaseOS/x86_64/os/Packages",
                "sha256": "7949b18b6d359b435686f2f5781928675ec8b2872b96f0abf6ba10747f794694",
                "name": "avahi-libs-0.7-19.el8.i686.rpm",
                "size": 68920,
            },
            {
                "path": "AppStream/s390x/os/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.s390x.rpm",
                "size": 29562,
            },
        ],
        "symlinks": [],
    }
    settings = get_settings(sys_args=["RHEL-8", "/tmp", "--variant", "Server"])[
        "topics"
    ][0]
    expected_files_list = {
        "directories": [],
        "files": [
            {
                "path": "",
                "sha256": "954719cab91afac5bc142656afff86e6d8e87570b035cbce65dbbb84892a40d3",
                "name": ".composeinfo",
                "size": 14496,
            }
        ],
        "symlinks": [],
    }
    assert filter_files_list(dci_files_list, settings) == expected_files_list


def test_filter_files_list_download_everything():
    dci_files_list = {
        "directories": [],
        "files": [
            {
                "path": "",
                "sha256": "954719cab91afac5bc142656afff86e6d8e87570b035cbce65dbbb84892a40d3",
                "name": ".composeinfo",
                "size": 14496,
            },
            {
                "path": "AppStream/x86_64/debug/tree/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.x86_64.rpm",
                "size": 45052,
            },
            {
                "path": "AppStream/x86_64/os/Packages",
                "sha256": "8fe293470f677bfc6eb04204c47b5e1a0e5d15431ef7ed9dbb269aaea386ed9f",
                "name": "PackageKit-command-not-found-1.1.12-2.el8.x86_64.rpm",
                "size": 28616,
            },
            {
                "path": "BaseOS/x86_64/os/Packages",
                "sha256": "7949b18b6d359b435686f2f5781928675ec8b2872b96f0abf6ba10747f794694",
                "name": "avahi-libs-0.7-19.el8.i686.rpm",
                "size": 68920,
            },
            {
                "path": "AppStream/s390x/os/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.s390x.rpm",
                "size": 29562,
            },
        ],
        "symlinks": [],
    }
    settings = get_settings(sys_args=["RHEL-8", "/tmp", "--all"])["topics"][0]
    expected_files_list = {
        "directories": [],
        "files": [
            {
                "path": "",
                "sha256": "954719cab91afac5bc142656afff86e6d8e87570b035cbce65dbbb84892a40d3",
                "name": ".composeinfo",
                "size": 14496,
            },
            {
                "path": "AppStream/x86_64/debug/tree/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.x86_64.rpm",
                "size": 45052,
            },
            {
                "path": "AppStream/x86_64/os/Packages",
                "sha256": "8fe293470f677bfc6eb04204c47b5e1a0e5d15431ef7ed9dbb269aaea386ed9f",
                "name": "PackageKit-command-not-found-1.1.12-2.el8.x86_64.rpm",
                "size": 28616,
            },
            {
                "path": "BaseOS/x86_64/os/Packages",
                "sha256": "7949b18b6d359b435686f2f5781928675ec8b2872b96f0abf6ba10747f794694",
                "name": "avahi-libs-0.7-19.el8.i686.rpm",
                "size": 68920,
            },
            {
                "path": "AppStream/s390x/os/Packages",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "PackageKit-command-not-found-debuginfo-1.1.12-2.el8.s390x.rpm",
                "size": 29562,
            },
        ],
        "symlinks": [],
    }
    assert filter_files_list(dci_files_list, settings) == expected_files_list


def test_nrt_always_download_metadata():
    dci_files_list = {
        "directories": [],
        "files": [
            {
                "path": "metadata",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "rpms.json",
                "size": 45052,
            },
        ],
        "symlinks": [],
    }
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp", "--variant", "AppStream"]
    )["topics"][0]
    expected_files_list = {
        "directories": [],
        "files": [
            {
                "path": "metadata",
                "sha256": "6f48f0d285918e502035da74decf447c6bb29898206406a4ed6a92ece94d276a",
                "name": "rpms.json",
                "size": 45052,
            },
        ],
        "symlinks": [],
    }
    assert filter_files_list(dci_files_list, settings) == expected_files_list
