import os

from dci_downloader.settings import (
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
        "local_repo_ip": "192.168.1.1",
        "systems": ["dci-client"],
        "topic": "RHEL-7.6",
        "variants": ["AppStream", "BaseOS"],
        "with_debug": False,
    }


def test_create_retro_compatible_variables_with_topic():
    settings = _create_retro_compatible_variables({"topic": "RHEL-7"})
    assert settings == {"topic": "RHEL-7", "topic_name": "RHEL-7"}


def test_create_retro_compatible_variables_with_destination():
    settings = _create_retro_compatible_variables({"destination": "/var/www/html"})
    assert settings == {
        "destination": "/var/www/html",
        "destination_folder": "/var/www/html",
    }


def test_get_settings_from_env_variables():
    settings = get_settings(
        sys_args=["RHEL-8", "/var/www/html"],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
        },
    )
    assert settings["remoteci_id"] == "9dd94b70-1707-46c5-a2bb-661e8d5d4212"
    assert settings["destination_folder"] == "/var/www/html"


def test_get_settings_transform_topic_in_topic_name():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "default_settings.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
        },
    )
    assert settings["topic_name"] == "RHEL-7"


def test_get_settings_read_arguments():
    settings = get_settings(
        sys_args=["RHEL-8", "/var/www/html", "--arch", "ppc64le"],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
        },
    )
    assert settings["archs"] == ["ppc64le"]


def test_get_settings_from_env_variables_retro_compatibility():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "default_settings.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-1707-46c5-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "/tmp/repo",
        },
    )
    assert settings["destination_folder"] == "/tmp/repo"
    assert settings["archs"] == ["x86_64"]
    assert settings["variants"] == []
    assert settings["remoteci_id"] == "9dd94b70-1707-46c5-a2bb-661e8d5d4212"
    assert not settings["download_everything"]
    assert not settings["with_debug"]
    assert settings["topic_name"] == "RHEL-7"
    assert settings["topic"] == "RHEL-7"


def test_get_settings_from_env_variables_retro_compatibility_rhel_agent_settings():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(test_dir, "data", "settings.yml")
    settings = get_settings(
        sys_args=["--settings", settings_file_path],
        env_variables={
            "DCI_CLIENT_ID": "remoteci/9dd94b70-46c5-1707-a2bb-661e8d5d4212",
            "DCI_API_SECRET": "",
            "DCI_CS_URL": "",
            "DCI_LOCAL_REPO": "/tmp/repo2",
        },
    )
    assert settings["destination_folder"] == "/tmp/repo2"
    assert settings["archs"] == ["x86_64", "ppc64le"]
    assert settings["variants"] == ["AppStream", "BaseOS"]
    assert settings["remoteci_id"] == "9dd94b70-46c5-1707-a2bb-661e8d5d4212"
    assert not settings["download_everything"]
    assert not settings["with_debug"]
    assert settings["topic_name"] == "RHEL-7.6"
    assert settings["topic"] == "RHEL-7.6"
