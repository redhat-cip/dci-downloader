import os
import pytest


from dci_downloader.settings import (
    _read_settings_files,
    get_settings,
    exit_if_settings_invalid,
    _variants_are_invalid,
)


def _topic_equals(topic, expected_topic):
    assert topic["name"] == expected_topic["name"]
    assert topic["download_folder"] == expected_topic["download_folder"]
    assert sorted(topic["archs"]) == sorted(expected_topic["archs"])
    assert sorted(topic["variants"], key=lambda v: v["name"]) == sorted(
        expected_topic["variants"], key=lambda v: v["name"]
    )
    assert topic["download_everything"] == expected_topic["download_everything"]


def test_read_settings_file_v1():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1.yml")
    settings = _read_settings_files([settings_file_path])
    assert settings == {"topic": "RHEL-7"}


def test_override_settings_file_v1():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_paths = [os.path.join(test_dir, "data", "settings_v1.yml")]
    settings_file_paths.append(os.path.join(test_dir, "data", "override_v1.yml"))
    settings = _read_settings_files(settings_file_paths)
    assert settings == {"topic": "RHEL-override"}


def test_read_settings_file_v2():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v2.yml")
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


def test_override_settings_file_v2():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_paths = [os.path.join(test_dir, "data", "settings_v2.yml")]
    settings_file_paths.append(os.path.join(test_dir, "data", "override_v2.yml"))
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


def test_read_settings_file_v3():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v3.yml")
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
                "variants": ["AppStream", {"name": "BaseOS", "with_debug": True, "with_iso": False}],
                "systems": ["SUT4"],
            },
        ],
    }


def test_override_settings_file_v3():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_paths = [os.path.join(test_dir, "data", "settings_v3.yml")]
    settings_file_paths.append(os.path.join(test_dir, "data", "override_v3.yml"))
    settings = _read_settings_files(settings_file_paths)
    assert settings == {
        "download_folder": "/tmp/override",
        "jobs": [
            {
                "topic": "RHEL-8.2",
                "archs": ["x86_64", "aarch64"],
                "variants": ["AppStream", {"name": "BaseOS", "with_debug": True, "with_iso": True}],
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
    _topic_equals(
        settings["topics"][0],
        {
            "download_everything": False,
            "download_folder": "/tmp/repo2",
            "name": "RHEL-8",
            "archs": ["ppc64le"],
            "variants": [{"name": "BaseOS", "with_debug": False, "with_iso": False}],
        },
    )


def test_get_settings_read_arguments_with_component_id():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo12", "--component-id", "c1"],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    assert settings["topics"][0]["component_id"] == "c1"


def test_get_settings_read_arguments_download_everything():
    settings = get_settings(
        sys_args=["RHEL-8", "/tmp/repo3", "--all"],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    _topic_equals(
        settings["topics"][0],
        {
            "download_everything": True,
            "download_folder": "/tmp/repo3",
            "name": "RHEL-8",
            "archs": ["x86_64"],
            "variants": [],
        },
    )


def test_get_settings_from_dci_rhel_agent_settings_file_with_only_topic_key():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v1.yml")
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
    _topic_equals(
        settings["topics"][0],
        {
            "download_everything": False,
            "download_folder": "/tmp/repo4",
            "name": "RHEL-7",
            "archs": ["x86_64"],
            "variants": [],
        },
    )


def test_get_settings_from_first_dci_rhel_agent_settings_file():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v2.yml")
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
    _topic_equals(
        settings["topics"][0],
        {
            "download_everything": False,
            "download_folder": "/tmp/repo5",
            "name": "RHEL-8.1",
            "archs": ["x86_64", "ppc64le"],
            "variants": [
                {"name": "AppStream", "with_debug": False, "with_iso": False},
                {"name": "BaseOS", "with_debug": False, "with_iso": False},
            ],
        },
    )


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
        settings_file_path = os.path.join(test_dir, "data", "settings_v2.yml")
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
    settings_file_path = os.path.join(test_dir, "data", "settings_v3.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    _topic_equals(
        settings["topics"][0],
        {
            "download_everything": False,
            "download_folder": "/tmp/repo10",
            "name": "RHEL-7.6",
            "archs": ["x86_64", "ppc64le"],
            "variants": [
                {"name": "Server", "with_debug": False, "with_iso": False},
                {"name": "Server-SAP", "with_debug": False, "with_iso": False},
            ],
        },
    )
    _topic_equals(
        settings["topics"][1],
        {
            "download_everything": False,
            "download_folder": "/tmp/repo10",
            "name": "RHEL-8.1",
            "archs": ["x86_64"],
            "variants": [
                {"name": "AppStream", "with_debug": False, "with_iso": False},
                {"name": "BaseOS", "with_debug": True, "with_iso": False},
            ],
        },
    )


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
    settings_file_path = os.path.join(test_dir, "data", "settings_v4.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "/tmp/repo4",
        },
    )
    _topic_equals(
        settings["topics"][0],
        {
            "download_everything": False,
            "download_folder": "/tmp/repo5",
            "name": "RHEL-8.2",
            "archs": ["x86_64", "ppc64le"],
            "variants": [
                {"name": "AppStream", "with_debug": False, "with_iso": False},
                {"name": "BaseOS", "with_debug": False, "with_iso": False},
            ],
        },
    )


def test_get_settings_local_repo_with_multiple_topics():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings_v5.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    _topic_equals(
        settings["topics"][0],
        {
            "download_everything": False,
            "download_folder": "/tmp/repo6",
            "name": "RHEL-7.6",
            "archs": ["x86_64"],
            "variants": [],
        },
    )
    _topic_equals(
        settings["topics"][1],
        {
            "download_everything": False,
            "download_folder": "/tmp/repo6",
            "name": "RHEL-8.1",
            "archs": ["x86_64"],
            "variants": [],
        },
    )


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
    settings_file_path = os.path.join(test_dir, "data", "settings_v6.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={"DCI_CLIENT_ID": "", "DCI_API_SECRET": "", "DCI_CS_URL": ""},
    )
    topic = settings["topics"][0]
    assert topic["dci_key_file"] == "/etc/dci-rhel-agent/dci.key"
    assert topic["dci_cert_file"] == "/etc/dci-rhel-agent/dci.crt"


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
