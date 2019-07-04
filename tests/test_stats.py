from dci_downloader.stats import get_component_size


def test_get_component_size():
    dci_files_list = {
        "directories": [],
        "files": [
            {
                "name": "a",
                "path": "",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "size": 456,
            },
            {
                "name": "b",
                "path": "",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "size": 1234,
            },
            {
                "name": "c",
                "path": "",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "size": 789,
            },
        ],
        "symlinks": [],
    }
    assert get_component_size(dci_files_list) == 2479
