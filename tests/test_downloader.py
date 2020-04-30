from mock import patch
from dci_downloader.downloader import download_component


@patch("dci_downloader.downloader.filter_files_list")
@patch("dci_downloader.downloader.check_download_folder_size")
@patch("dci_downloader.downloader.get_files_list")
def test_download_component_filter_compose_component(
    get_files_list, check_download_folder_size, filter_files_list
):
    component = {
        "id": "c1",
        "name": "RHEL-8.2.0-20191120.0",
        "type": "Compose",
        "topic_id": "t1",
    }
    topic = {"id": "t1", "name": "RHEL-8", "product_id": "p1"}
    settings = {
        "component_id": "c1",
        "download_folder": "/var/www/html",
    }
    cert = "/tmp/cert"
    key = "/tmp/key"
    download_component(topic, component, settings, cert, key)
    filter_files_list.assert_called_once()


@patch("dci_downloader.downloader.filter_files_list")
@patch("dci_downloader.downloader.check_download_folder_size")
@patch("dci_downloader.downloader.get_files_list")
def test_download_component_not_filter_puddle_osp_component(
    get_files_list, check_download_folder_size, filter_files_list
):
    component = {
        "id": "c1",
        "name": "RH7-RHOS-13.0 2020-04-01.3",
        "type": "puddle_osp",
        "topic_id": "t1",
    }
    topic = {"id": "t1", "name": "OSP13", "product_id": "p1"}
    settings = {
        "component_id": "c1",
        "download_folder": "/var/www/html",
    }
    cert = "/tmp/cert"
    key = "/tmp/key"
    download_component(topic, component, settings, cert, key)
    filter_files_list.assert_not_called()
