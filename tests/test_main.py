import pytest
import mock

from dci_downloader.main import download_components


def test_download_one_component_if_component_id():
    api = mock.MagicMock()
    topic = {"id": "t1", "name": "RHEL-8"}
    api.get_topic.return_value = topic
    component = {"id": "c1", "name": "RHEL-8.2.0-20191120.0", "topic_id": "t1"}
    api.get_component_by_id.return_value = component
    downloader = mock.MagicMock()
    settings = {
        "name": "RHEL-8",
        "component_id": "c1",
        "download_folder": "/var/www/html",
    }
    cert = "/tmp/cert"
    key = "/tmp/key"
    download_components(settings, api, downloader, cert, key)
    api.get_topic.assert_called_once_with("RHEL-8")
    api.get_components.assert_called_once_with(topic)
    downloader.download_component.assert_called_once_with(
        topic, component, settings, cert, key
    )


def test_download_components_if_no_component_id():
    api = mock.MagicMock()
    topic = {"id": "t1", "name": "RHEL-8"}
    api.get_topic.return_value = topic
    component1 = {"id": "c1", "name": "RHEL-8.2.0-20191120.0", "topic_id": "t1"}
    component2 = {"id": "c2", "name": "hwcert-1575558974", "topic_id": "t1"}
    api.get_components.return_value = [component1, component2]
    downloader = mock.MagicMock()
    settings = {
        "name": "RHEL-8",
        "download_folder": "/var/www/html",
    }
    cert = "/tmp/cert"
    key = "/tmp/key"
    download_components(settings, api, downloader, cert, key)
    api.get_topic.assert_called_once_with("RHEL-8")
    downloader.download_component.assert_has_calls(
        [
            mock.call(topic, component1, settings, cert, key),
            mock.call(topic, component2, settings, cert, key),
        ]
    )


def test_download_with_wrong_component_id_raised_an_error():
    api = mock.MagicMock()
    topic = {"id": "t1", "name": "RHEL-8"}
    api.get_topic.return_value = topic
    component1 = {"id": "c1", "name": "RHEL-8.2.0-20191120.0", "topic_id": "t2"}
    component2 = {"id": "c2", "name": "hwcert-1575558974", "topic_id": "t2"}
    api.get_components.return_value = [component1, component2]
    downloader = mock.MagicMock()
    settings = {
        "name": "RHEL-8",
        "component_id": "c3",
        "download_folder": "/var/www/html",
    }
    cert = "/tmp/cert"
    key = "/tmp/key"
    with pytest.raises(Exception):
        download_components(settings, api, downloader, cert, key)
    api.get_topic.assert_called_once_with("RHEL-8")
    api.get_components.assert_called_once_with(topic)
