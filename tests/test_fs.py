from dci_downloader.fs import build_download_folder


def test_build_download_folder():
    topic = {"id": "t1", "name": "topic 1"}
    component = {"id": "c1", "type": "Compose"}
    download_folder = build_download_folder(topic, component, "/var/www/html")
    expected_download_folder = "/var/www/html/topic_1/compose"
    assert download_folder == expected_download_folder
