from dci_downloader.fs import build_destination_folder


def test_get_base_url():
    topic = {"id": "t1", "name": "topic 1"}
    component = {"id": "c1", "type": "Compose"}
    local_storage_folder = "/var/www/html"
    destination_folder = build_destination_folder(
        topic, component, local_storage_folder
    )
    expected_destination_folder = "/var/www/html/topic_1/compose"
    assert destination_folder == expected_destination_folder
