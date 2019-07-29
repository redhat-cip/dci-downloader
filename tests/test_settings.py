import os

from dcidownloader.settings import (
    _read_settings_file,
    _create_retro_compatible_variables,
    get_settings,
)


def test_reading_empty_settings_file():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "default_settings.yml")
    settings = _read_settings_file(settings_file_path)
    assert settings == {"topic": "RHEL-7"}


def test_reading_settings_file():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings.yml")
    settings = _read_settings_file(settings_file_path)
    assert settings == {
        "archs": ["x86_64", "ppc64le"],
        "dci_rhel_agent_cert": False,
        "download_only": False,
        "local_repo_ip": "172.23.100.100",
        "systems": ["labvm.local"],
        "topic": "RHEL-7",
        "variants": ["AppStream", "BaseOS"],
        "with_debug": False,
    }


def test_create_retro_compatible_variables_with_topic():
    settings = _create_retro_compatible_variables({"topic": "RHEL-7"})
    assert settings == {"topic": "RHEL-7", "topics_names": ["RHEL-7"]}


def test_create_retro_compatible_variables_with_topics():
    settings = _create_retro_compatible_variables({"topics": ["RHEL-7", "RHEL-8"]})
    assert settings == {
        "topics": ["RHEL-7", "RHEL-8"],
        "topics_names": ["RHEL-7", "RHEL-8"],
    }


def test_get_settings_from_env_variables():
    settings = get_settings(
        sys_args=[],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "/var/www/html",
        },
    )
    assert settings["remoteci_id"] == "9dd94b70-1707-46c5-a2bb-661e8d5d4212"
    assert settings["local_storage_folder"] == "/var/www/html"


def test_get_settings_transform_topic_in_topics_names():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "default_settings.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "",
        },
    )
    assert settings["topics_names"] == ["RHEL-7"]


def test_get_settings_read_arguments():
    settings = get_settings(
        sys_args=["--arch", "ppc64le"],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "",
        },
    )
    assert settings["archs"] == ["ppc64le"]
