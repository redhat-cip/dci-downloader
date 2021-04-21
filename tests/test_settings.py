import os
import mock
import pytest

from dci_downloader.settings import (
    _read_settings_files,
    _variants_are_invalid,
    exit_if_settings_invalid,
    get_settings,
)
from mock import ANY


def test_read_settings_file_v1a():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1a.yml")
    settings = _read_settings_files([settings_file_path])
    assert settings == {"topic": "RHEL-7"}


def test_override_settings_file_v1a():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_paths = [os.path.join(test_dir, "data", "settings_v1a.yml")]
    settings_file_paths.append(os.path.join(test_dir, "data", "override_v1a.yml"))
    settings = _read_settings_files(settings_file_paths)
    assert settings == {"topic": "RHEL-override"}


def test_read_settings_file_v1b():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1b.yml")
    settings = _read_settings_files([settings_file_path])
    assert settings == {
        "archs": ["x86_64", "ppc64le"],
        "dci_rhel_agent_cert": False,
        "local_repo_ip": "192.168.1.1",
        "systems": ["dci-client"],
        "topic": "RHEL-8.1",
        "variants": ["AppStream", "BaseOS"],
        "with_debug": False,
        "with_iso": False,
    }


def test_override_settings_file_v1b():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_paths = [os.path.join(test_dir, "data", "settings_v1b.yml")]
    settings_file_paths.append(os.path.join(test_dir, "data", "override_v1b.yml"))
    settings = _read_settings_files(settings_file_paths)
    assert settings == {
        "archs": ["x86_64", "ppc64le"],
        "dci_rhel_agent_cert": False,
        "local_repo_ip": "192.168.1.1",
        "systems": ["dci-client"],
        "topic": "RHEL-override",
        "variants": ["AppStream", "BaseOS"],
        "with_debug": False,
        "with_iso": True,
    }


def test_read_settings_file_v1c():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1c.yml")
    settings = _read_settings_files([settings_file_path])
    assert settings == {
        "download_folder": "/tmp/repo10",
        "jobs": [
            {
                "topic": "RHEL-7.6",
                "archs": ["x86_64", "ppc64le"],
                "variants": ["Server", "Server-SAP"],
                "tags": ["my_tag_1", "my_tag_2"],
                "tests": ["rhcert", "hardware_cert"],
                "systems": ["SUT1", "SUT2", "SUT3"],
            },
            {
                "topic": "RHEL-8.1",
                "archs": ["x86_64"],
                "variants": [
                    "AppStream",
                    {"name": "BaseOS", "with_debug": True, "with_iso": False},
                ],
                "systems": ["SUT4"],
            },
        ],
    }


def test_override_settings_file_v1c():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_paths = [os.path.join(test_dir, "data", "settings_v1c.yml")]
    settings_file_paths.append(os.path.join(test_dir, "data", "override_v1c.yml"))
    settings = _read_settings_files(settings_file_paths)
    assert settings == {
        "download_folder": "/tmp/override",
        "jobs": [
            {
                "topic": "RHEL-8.2",
                "archs": ["x86_64", "aarch64"],
                "variants": [
                    "AppStream",
                    {"name": "BaseOS", "with_debug": True, "with_iso": True},
                ],
                "systems": ["SUT4"],
            },
        ],
    }


def test_get_settings_set_remoteci_id_from_env_variable():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo1"],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
        },
    )
    assert settings["remoteci_id"] == "9dd94b70-1707-46c5-a2bb-661e8d5d4212"


def test_get_settings_read_arguments():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo2", "--arch", "ppc64le", "--variant", "BaseOS"],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    assert settings["topics"][0] == {
        "variants": [{"name": "BaseOS", "with_debug": False, "with_iso": False}],
        "download_everything": False,
        "download_folder": "/tmp/repo2",
        "archs": ["ppc64le"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-8",
        "with_debug": False,
        "registry": None,
        "tags": [],
    }
    assert settings["version"] == 1


def test_get_settings_read_arguments_with_component_id():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo12", "--component-id", "c1"],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    assert settings["topics"][0]["component_id"] == "c1"
    assert settings["version"] == 1


def test_get_settings_read_arguments_download_everything():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo3", "--all"],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    assert settings["topics"][0] == {
        "variants": [],
        "download_everything": True,
        "download_folder": "/tmp/repo3",
        "archs": ["x86_64"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-8",
        "with_debug": False,
        "registry": None,
        "tags": [],
    }
    assert settings["version"] == 1


def test_get_settings_from_dci_rhel_agent_settings_file_with_only_topic_key():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1a.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "/tmp/repo4",
        },
    )

    assert settings["remoteci_id"] == "9dd94b70-1707-46c5-a2bb-661e8d5d4212"
    assert settings["topics"][0] == {
        "variants": [],
        "download_everything": False,
        "download_folder": "/tmp/repo4",
        "archs": ["x86_64"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-7",
        "with_debug": False,
        "registry": None,
        "tags": [],
    }
    assert settings["version"] == 1


def test_get_settings_from_first_dci_rhel_agent_settings_file():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1b.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/66194b70-46c5-1707-a2bb-9dde8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "/tmp/repo5",
        },
    )
    assert settings["remoteci_id"] == "66194b70-46c5-1707-a2bb-9dde8d5d4212"
    assert settings["topics"][0] == {
        "variants": [
            {"name": "AppStream", "with_debug": False, "with_iso": False},
            {"name": "BaseOS", "with_debug": False, "with_iso": False},
        ],
        "download_everything": False,
        "download_folder": "/tmp/repo5",
        "archs": ["x86_64", "ppc64le"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-8.1",
        "with_debug": False,
        "registry": None,
        "tags": [],
    }
    assert settings["version"] == 1


def test_get_settings_add_env_variables():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo6"],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "jSbJwfCdIfq12gwHAAtg5JXSBTO3wj0xkG7oW3DlqyM7bXahPRrfZlqmSv3BhmAy",
            "DCI_CS_URL": "https://distributed-ci.io",
        },
    )
    assert settings["env_variables"] == {
        "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
        "DCI_API_SECRET": "jSbJwfCdIfq12gwHAAtg5JXSBTO3wj0xkG7oW3DlqyM7bXahPRrfZlqmSv3BhmAy",
        "DCI_CS_URL": "https://distributed-ci.io",
    }


def test_exit_if_settings_invalid():
    try:
        exit_if_settings_invalid(
            get_settings(
                sys_args=["RHEL-8", "/tmp/repo7", "--variant", "BaseOS"],
                env_variables={
                    "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
                    "DCI_API_SECRET": "jSbJwfCdIfq12gwHAAtg5JXSBTO3wj0xkG7oW3DlqyM7bXahPRrfZlqmSv3BhmAy",
                    "DCI_CS_URL": "https://distributed-ci.io",
                },
            )
        )
    except SystemExit:
        pytest.fail("exit_if_settings_invalid raise SystemExit but should not")


def test_exit_if_settings_invalid_with_empty_env_variables():
    with pytest.raises(SystemExit):
        exit_if_settings_invalid(
            get_settings(sys_args=["RHEL-8", "/tmp/repo8"], env_variables={})
        )


def test_exit_if_settings_invalid_without_download_folder():
    with pytest.raises(SystemExit):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file_path = os.path.join(test_dir, "data", "settings_v1b.yml")
        exit_if_settings_invalid(
            get_settings(
                sys_args=["--settings", settings_file_path],
                env_variables={
                    "DCI_CLIENT_ID": "remoteci/66194b70-46c5-1707-a2bb-9dde8d5d4212",
                    "DCI_API_SECRET": "",
                    "DCI_CS_URL": "",
                },
            )
        )


def test_exit_if_settings_invalid_with_bad_variants():
    with pytest.raises(SystemExit):
        exit_if_settings_invalid(
            get_settings(
                sys_args=[
                    "RHEL-8",
                    "/tmp/repo9",
                    "--variant",
                    "AppStream",
                    "--variant",
                    "Server",
                ],
                env_variables={
                    "DCI_CLIENT_ID": "",
                    "DCI_API_SECRET": "",
                    "DCI_CS_URL": "",
                },
            )
        )


def test_get_settings_with_jobs_key():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1c.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    assert settings["topics"][0] == {
        "variants": [
            {"name": "Server", "with_debug": False, "with_iso": False},
            {"name": "Server-SAP", "with_debug": False, "with_iso": False},
        ],
        "download_everything": False,
        "download_folder": "/tmp/repo10",
        "archs": ["x86_64", "ppc64le"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-7.6",
        "with_debug": False,
        "registry": None,
        "tags": ["my_tag_1", "my_tag_2"],
    }
    assert settings["topics"][1] == {
        "variants": [
            {"name": "AppStream", "with_debug": False, "with_iso": False},
            {"name": "BaseOS", "with_debug": True, "with_iso": False},
        ],
        "download_everything": False,
        "download_folder": "/tmp/repo10",
        "archs": ["x86_64"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-8.1",
        "with_debug": False,
        "registry": None,
        "tags": [],
    }
    assert settings["version"] == 1


def test_get_settings_download_folder_overwrite_DCI_LOCAL_REPO():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "documented_settings_file.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "/tmp/repo4",
        },
    )
    assert settings["topics"][0]["download_folder"] == "/var/www/html"
    assert settings["topics"][1]["download_folder"] == "/var/www/html"


def test_get_settings_local_repo_added_to_an_old_settings_file():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1d.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "/tmp/repo4",
        },
    )
    assert settings["topics"][0] == {
        "variants": [
            {"name": "AppStream", "with_debug": False, "with_iso": False},
            {"name": "BaseOS", "with_debug": False, "with_iso": False},
        ],
        "download_everything": False,
        "download_folder": "/tmp/repo5",
        "archs": ["x86_64", "ppc64le"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-8.2",
        "with_debug": False,
        "registry": None,
        "tags": [],
    }
    assert settings["version"] == 1


def test_get_settings_local_repo_with_multiple_topics():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1e.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    assert settings["topics"][0] == {
        "variants": [],
        "download_everything": False,
        "download_folder": "/tmp/repo6",
        "archs": ["x86_64"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-7.6",
        "with_debug": False,
        "registry": None,
        "tags": [],
    }
    assert settings["topics"][1] == {
        "variants": [],
        "download_everything": False,
        "download_folder": "/tmp/repo6",
        "archs": ["x86_64"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-8.1",
        "with_debug": False,
        "registry": None,
        "tags": [],
    }
    assert settings["version"] == 1


def test_backward_compatibility_test_variants_are_invalid_with_metadata():
    assert (
        _variants_are_invalid({"name": "RHEL-7", "variants": [{"name": "metadata"}]})
        is False
    )
    assert (
        _variants_are_invalid({"name": "RHEL-8", "variants": [{"name": "metadata"}]})
        is False
    )


def test_get_settings_set_ssl_files_to_default_if_not_setted():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo1"],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "XDG_DATA_HOME": "/home/dci/.local/share",
        },
    )
    topic = settings["topics"][0]
    assert topic["dci_cert_file"] == "/home/dci/.local/share/dci-downloader/dci.crt"
    assert topic["dci_key_file"] == "/home/dci/.local/share/dci-downloader/dci.key"


def test_get_settings_set_ssl_file_from_env():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo1"],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_KEY_FILE": "/etc/dci-rhel-agent/dci.key",
            "DCI_CERT_FILE": "/etc/dci-rhel-agent/dci.crt",
        },
    )
    topic = settings["topics"][0]
    assert topic["dci_key_file"] == "/etc/dci-rhel-agent/dci.key"
    assert topic["dci_cert_file"] == "/etc/dci-rhel-agent/dci.crt"


def test_get_settings_set_ssl_file_from_settings_file():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1f.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    topic = settings["topics"][0]
    assert topic["dci_key_file"] == "/etc/dci-rhel-agent/dci.key"
    assert topic["dci_cert_file"] == "/etc/dci-rhel-agent/dci.crt"


def test_get_settings_with_debug_without_a_variant():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1g.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    assert settings["topics"][0] == {
        "variants": [],
        "download_everything": False,
        "download_folder": "/var/www/html",
        "archs": ["ppc64le"],
        "component_id": None,
        "dci_key_file": ANY,
        "components": [],
        "dci_cert_file": ANY,
        "name": "RHEL-8.2-milestone",
        "with_debug": True,
        "registry": None,
        "tags": [],
    }
    assert settings["version"] == 1


def test_exit_if_architecture_in_settings_invalid():
    with pytest.raises(SystemExit):
        exit_if_settings_invalid(
            get_settings(
                sys_args=["RHEL-8", "/tmp/repo7", "--arch", "x86"],
                env_variables={
                    "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
                    "DCI_API_SECRET": "jSbJwfCdIfq12gwHAAtg5JXSBTO3wj0xkG7oW3DlqyM7bXahPRrfZlqmSv3BhmAy",
                    "DCI_CS_URL": "https://distributed-ci.io",
                },
            )
        )


def test_exit_if_architecture_in_settings_invalid_for_rhel_7():
    with pytest.raises(SystemExit):
        exit_if_settings_invalid(
            get_settings(
                sys_args=["RHEL-7", "/tmp/repo7", "--arch", "aarch64"],
                env_variables={
                    "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
                    "DCI_API_SECRET": "jSbJwfCdIfq12gwHAAtg5JXSBTO3wj0xkG7oW3DlqyM7bXahPRrfZlqmSv3BhmAy",
                    "DCI_CS_URL": "https://distributed-ci.io",
                },
            )
        )


@mock.patch("dci_downloader.settings.has_skopeo_command")
def test_exit_if_registry_and_no_skopeo(has_skopeo_command_mock):
    has_skopeo_command_mock.return_value = False
    with pytest.raises(SystemExit):
        exit_if_settings_invalid(
            get_settings(
                sys_args=[
                    "OSP16.2",
                    "/tmp/repoOSP16.2",
                    "--registry",
                    "localhost:5000",
                ],
                env_variables={
                    "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
                    "DCI_API_SECRET": "jSbJwfCdIfq12gwHAAtg5JXSBTO3wj0xkG7oW3DlqyM7bXahPRrfZlqmSv3BhmAy",
                    "DCI_CS_URL": "https://distributed-ci.io",
                },
            )
        )


@mock.patch("dci_downloader.settings.has_skopeo_command")
def test_with_registry_and_skopeo(has_skopeo_command_mock):
    has_skopeo_command_mock.return_value = True
    exit_if_settings_invalid(
        get_settings(
            sys_args=["OSP16.2", "/tmp/repoOSP16.2", "--registry", "localhost:5000"],
            env_variables={
                "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
                "DCI_API_SECRET": "jSbJwfCdIfq12gwHAAtg5JXSBTO3wj0xkG7oW3DlqyM7bXahPRrfZlqmSv3BhmAy",
                "DCI_CS_URL": "https://distributed-ci.io",
            },
        )
    )


def test_with_registry():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo1", "--registry", "host:port"],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "XDG_DATA_HOME": "/home/dci/.local/share",
        },
    )
    topic = settings["topics"][0]
    assert topic["registry"] == "host:port"


def test_get_settings_v2():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v2.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )

    assert settings == {
        "registry": None,
        "dci_cert_file": ANY,
        "topics": [
            {
                "registry": None,
                "components": [],
                "variants": [],
                "name": "RHEL-9.0",
                "dci_cert_file": ANY,
                "archs": ["x86_64"],
                "download_everything": False,
                "with_debug": False,
                "download_folder": "/var/www/html",
                "component_id": None,
                "dci_key_file": ANY,
                "tags": ["nightly"],
            },
            {
                "registry": None,
                "components": [],
                "variants": [
                    {"name": "AppStream", "with_iso": False, "with_debug": False},
                    {"name": "BaseOS", "with_debug": True},
                ],
                "name": "RHEL-8.4",
                "dci_cert_file": ANY,
                "archs": ["ppc64le"],
                "download_everything": False,
                "with_debug": False,
                "download_folder": "/var/www/html",
                "component_id": None,
                "dci_key_file": ANY,
                "tags": ["milestone"],
            },
            {
                "registry": None,
                "components": [],
                "variants": [],
                "name": "RHEL-8.2",
                "dci_cert_file": ANY,
                "archs": ["x86_64"],
                "download_everything": False,
                "with_debug": False,
                "download_folder": "/var/www/html",
                "component_id": None,
                "dci_key_file": ANY,
                "tags": [],
            },
        ],
        "dci_key_file": ANY,
        "remoteci_id": None,
        "env_variables": {"DCI_API_SECRET": "", "DCI_CLIENT_ID": "", "DCI_CS_URL": ""},
        "download_folder": "/var/www/html",
        "version": 2,
    }
