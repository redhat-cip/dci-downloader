import mock

from dci_downloader.main import download_components


@mock.patch("dci_downloader.main.api")
@mock.patch("dci_downloader.main.downloader")
def test_download_components_if_no_component_id(downloader_mock, api_mock):
    topic = {"id": "t1", "name": "RHEL-8"}
    api_mock.get_topic.return_value = topic
    component1 = {"id": "c1", "name": "RHEL-8.2.0-20191120.0", "topic_id": "t1"}
    component2 = {"id": "c2", "name": "hwcert-1575558974", "topic_id": "t1"}
    api_mock.get_components.return_value = [component1, component2]
    settings = {
        "name": "RHEL-8",
        "download_folder": "/var/www/html",
    }
    download_components(settings)
    api_mock.get_topic.assert_called_once_with("RHEL-8")
    downloader_mock.download_component.assert_has_calls(
        [
            mock.call(topic, component1, settings),
            mock.call(topic, component2, settings),
        ]
    )


@mock.patch("dci_downloader.main.api")
@mock.patch("dci_downloader.main.downloader")
def test_download_one_component_if_component_id(downloader_mock, api_mock):
    component = {"id": "c1", "name": "RHEL-8.2.0-20191120.0", "topic_id": "t1"}
    api_mock.get_component_by_id.return_value = component
    topic = {"id": "t1", "name": "RHEL-8"}
    api_mock.get_topic_by_id.return_value = topic
    settings = {
        "component_id": "c1",
        "download_folder": "/var/www/html",
    }
    download_components(settings)
    api_mock.get_component_by_id.assert_called_once_with(component["id"])
    api_mock.get_topic_by_id.assert_called_once_with(topic["id"])
    downloader_mock.download_component.assert_called_once_with(
        topic, component, settings
    )
