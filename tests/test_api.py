from dci_downloader.api import get_base_url


# gvincent: test fragile, testing implementation details
def test_get_base_url():
    topic = {"id": "t1", "product_id": "p1"}
    component = {"id": "c1"}
    topic_info = {"repo_url": "https://repo.distributed-ci.io"}
    assert (
        get_base_url(topic_info, topic, component)
        == "https://repo.distributed-ci.io/p1/t1/c1"
    )
