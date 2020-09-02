from dci_downloader.fs import get_component_folder, get_topic_folder


def test_get_component_folder():
    settings = {"name": "topic 1", "download_folder": "/var/www/html"}
    component = {"id": "c1", "type": "Compose"}
    download_folder = get_component_folder(settings, component)
    assert download_folder == "/var/www/html/topic_1/compose"


def test_get_topic_folder():
    settings = {"name": "topic 1", "download_folder": "/var/www/html"}
    assert get_topic_folder(settings) == "/var/www/html/topic_1"
