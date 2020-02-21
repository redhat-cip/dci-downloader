from dci_downloader.stats import get_component_size, get_sha256


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


def test_get_sha256(tmpdir):
    file_list = tmpdir.join("dci_files_list.json")
    file_list.write(
        """{
  "directories": [],
  "files": [],
  "symlinks": []
}"""
    )
    import os
    with open(os.path.join(file_list.dirname, file_list.basename)) as f:
        print(f.read().encode('utf-8'))
    assert (
        get_sha256(os.path.join(file_list.dirname, file_list.basename))
        == "3a93cc3078379d056a912c4567776a3c6b2688c25b998f85180a642ef3947a6a"
    )
