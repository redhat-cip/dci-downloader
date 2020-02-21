import requests
from mock import patch
from dci_downloader.api import get_base_url, get_files_list


def test_get_base_url():
    topic = {"id": "t1", "product_id": "p1"}
    component = {"id": "c1"}
    assert get_base_url(topic, component) == "https://repo.distributed-ci.io/p1/t1/c1"


@patch(
    "dci_downloader.api._download_files_list",
    return_value={"directories": [], "files": [], "symlinks": []},
)
def test_get_files_list_if_doesnt_exists_locally(mocked_download_files_list, tmpdir):
    base_url = "https://repo.example.org"
    assert get_files_list(tmpdir, base_url) == {
        "directories": [],
        "files": [],
        "symlinks": [],
    }
    mocked_download_files_list.assert_called_once()


@patch(
    "dci_downloader.api._download_files_list_checksum",
    return_value="3a93cc3078379d056a912c4567776a3c6b2688c25b998f85180a642ef3947a6a",
)
@patch("dci_downloader.api._download_files_list", return_value={})
def test_doesnt_get_files_list_if_exists_locally(
    mocked_download_files_list, mocked_download_files_list_checksum, tmpdir
):
    file_list = tmpdir.join("dci_files_list.json")
    file_list.write(
        """{
  "directories": [],
  "files": [],
  "symlinks": []
}"""
    )
    base_url = "https://repo.example.org"
    assert get_files_list(tmpdir, base_url) == {
        "directories": [],
        "files": [],
        "symlinks": [],
    }
    mocked_download_files_list_checksum.assert_called_once()
    mocked_download_files_list.assert_not_called()


@patch(
    "dci_downloader.api._download_files_list_checksum",
    return_value="18f8e7caf350caf5619ae91782bc464bb504fc82401233d2f73fb819a6aeb70c",
)
@patch(
    "dci_downloader.api._download_files_list",
    return_value={
        "directories": [],
        "files": [
            {
                "name": "a",
                "path": "",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "size": 0,
            }
        ],
        "symlinks": [],
    },
)
def test_get_files_list_if_exists_locally_but_content_different(
    mocked_download_files_list, mocked_download_files_list_checksum, tmpdir
):
    file_list = tmpdir.join("dci_files_list.json")
    file_list.write(
        """{
  "directories": [],
  "files": [],
  "symlinks": []
}"""
    )
    base_url = "https://repo.example.org"
    assert get_files_list(tmpdir, base_url) == {
        "directories": [],
        "files": [
            {
                "name": "a",
                "path": "",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "size": 0,
            }
        ],
        "symlinks": [],
    }
    mocked_download_files_list_checksum.assert_called_once()
    mocked_download_files_list.assert_called_once()


@patch(
    "dci_downloader.api._download_files_list_checksum",
    side_effect=requests.exceptions.HTTPError,
)
@patch(
    "dci_downloader.api._download_files_list",
    return_value={
        "directories": [],
        "files": [
            {
                "name": "a",
                "path": "",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "size": 0,
            }
        ],
        "symlinks": [],
    },
)
def test_get_files_list_if_checksum_doesnt_exists_yet(
    mocked_download_files_list, mocked_download_files_list_checksum, tmpdir
):
    file_list = tmpdir.join("dci_files_list.json")
    file_list.write(
        """{
  "directories": [],
  "files": [],
  "symlinks": []
}"""
    )
    base_url = "https://repo.example.org"
    assert get_files_list(tmpdir, base_url) == {
        "directories": [],
        "files": [
            {
                "name": "a",
                "path": "",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "size": 0,
            }
        ],
        "symlinks": [],
    }
    mocked_download_files_list_checksum.assert_called_once()
    mocked_download_files_list.assert_called_once()
