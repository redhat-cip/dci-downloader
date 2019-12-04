import os
import pytest

from dci_downloader.fs import build_download_folder, create_temp_file


def test_get_base_url():
    topic = {"id": "t1", "name": "topic 1"}
    component = {"id": "c1", "type": "Compose"}
    download_folder = build_download_folder(topic, component, "/var/www/html")
    expected_download_folder = "/var/www/html/topic_1/compose"
    assert download_folder == expected_download_folder


def test_create_temp_file_with_non_bytes_input():
    try:
        content = u"test"
        cert = create_temp_file(content)
        os.remove(cert.name)
    except TypeError:
        pytest.fail(
            "test_create_temp_file_with_non_bytes_input "
            "raise TypeError but should not"
        )
