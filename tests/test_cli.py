from dci_downloader.cli import parse_arguments


def test_parsing_empty_arguments():
    assert parse_arguments([]) == {"topics": {}}


def test_parsing_1_topic():
    arguments = parse_arguments(["--topic", "RHEL-7.6"])
    assert arguments["topics"] == {"RHEL-7.6": {"name": "RHEL-7.6"}}


def test_parsing_2_topics():
    arguments = parse_arguments(["--topic", "RHEL-7.6", "--topic", "RHEL-7.7"])
    assert arguments["topics"] == {
        "RHEL-7.6": {"name": "RHEL-7.6"},
        "RHEL-7.7": {"name": "RHEL-7.7"},
    }
