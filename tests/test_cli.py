from dcidownloader.cli import parse_arguments


def test_parsing_empty_arguments():
    args = parse_arguments([])
    assert args["topics_names"] == []
    assert args["archs"] == ["x86_64"]
    assert args["variants"] == []
    assert not args["with_debug"]
    assert args["settings"] is None


def test_parsing_download_all_argument():
    args = parse_arguments(["--all"])
    assert args["download_everything"]


def test_parsing_with_debug():
    args = parse_arguments(["--debug"])
    assert args["with_debug"]


def test_parsing_1_topic():
    args = parse_arguments(["--topic", "RHEL-7.6"])
    assert args["topics_names"] == ["RHEL-7.6"]


def test_parsing_2_topics():
    args = parse_arguments(["--topic", "RHEL-7.6", "--topic", "RHEL-7.7"])
    assert sorted(args["topics_names"]) == ["RHEL-7.6", "RHEL-7.7"]


def test_parsing_1_variant():
    args = parse_arguments(["--variant", "BaseOs"])
    assert args["variants"] == ["BaseOs"]


def test_parsing_2_variants():
    args = parse_arguments(["--variant", "BaseOs", "--variant", "AppStream"])
    assert sorted(args["variants"]) == ["AppStream", "BaseOs"]


def test_parsing_1_arch():
    args = parse_arguments(["--arch", "ppc64le"])
    assert args["archs"] == ["ppc64le"]


def test_parsing_2_archs():
    args = parse_arguments(["--arch", "x86_64", "--arch", "ppc64le"])
    assert sorted(args["archs"]) == ["ppc64le", "x86_64"]


def test_parsing_combined_arguments():
    args = parse_arguments(
        [
            "--topic",
            "RHEL-8.1",
            "--variant",
            "BaseOs",
            "--variant",
            "AppStream",
            "--arch",
            "x86_64",
        ]
    )
    assert sorted(args["topics_names"]) == ["RHEL-8.1"]
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"]) == ["AppStream", "BaseOs"]
    assert not args["with_debug"]


def test_parsing_arguments_dict():
    args = parse_arguments(
        [
            "--topic",
            "RHEL-8.1",
            "--variant",
            "BaseOs",
            "--variant",
            "AppStream",
            "--arch",
            "x86_64",
        ]
    )
    assert sorted(args["topics_names"]) == ["RHEL-8.1"]
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"]) == ["AppStream", "BaseOs"]
    assert not args["with_debug"]
