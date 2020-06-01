import mock

from dci_downloader.main import download_components


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
    download_components(settings, api, downloader)
    api.get_topic.assert_called_once_with("RHEL-8")
    downloader.download_component.assert_has_calls(
        [
            mock.call(topic, component1, settings),
            mock.call(topic, component2, settings),
        ]
    )


def test_download_one_component_if_component_id():
    api = mock.MagicMock()
    component = {"id": "c1", "name": "RHEL-8.2.0-20191120.0", "topic_id": "t1"}
    api.get_component_by_id.return_value = component
    topic = {"id": "t1", "name": "RHEL-8"}
    api.get_topic_by_id.return_value = topic
    downloader = mock.MagicMock()
    settings = {
        "component_id": "c1",
        "download_folder": "/var/www/html",
    }
    download_components(settings, api, downloader)
    api.get_component_by_id.assert_called_once_with(component["id"])
    api.get_topic_by_id.assert_called_once_with(topic["id"])
    downloader.download_component.assert_called_once_with(topic, component, settings)
