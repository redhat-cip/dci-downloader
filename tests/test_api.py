from dci_downloader.api import get_base_url


def test_get_base_url():
    topic = {"id": "t1", "product_id": "p1"}
    component = {"id": "c1"}
    assert get_base_url(topic, component) == "https://repo.distributed-ci.io/p1/t1/c1"
