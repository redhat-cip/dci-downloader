from pytest import raises
from dci_downloader.cli import parse_arguments


def test_parsing_no_options():
    args = parse_arguments(["RHEL-8", "/var/www/html"])
    assert args["topic_name"] == "RHEL-8"
    assert args["archs"] == ["x86_64"]
    assert args["variants"] == []
    assert not args["with_debug"]
    assert args["settings_file_path"] is None
    assert args["destination_folder"] == "/var/www/html"


def test_parsing_settings_file():
    args = parse_arguments(["--settings", "/etc/dci-downloader/settings.yml"])
    assert args["topic_name"] is None
    assert args["archs"] == ["x86_64"]
    assert args["variants"] == []
    assert not args["with_debug"]
    assert args["settings_file_path"] == "/etc/dci-downloader/settings.yml"
    assert args["destination_folder"] is None


def test_parsing_no_option_raise_exception():
    with raises(SystemExit):
        parse_arguments([])


def test_parsing_download_all_argument():
    args = parse_arguments(["RHEL-8", "/var/www/html", "--all"])
    assert args["download_everything"]


def test_parsing_with_debug():
    args = parse_arguments(["RHEL-8", "/var/www/html", "--debug"])
    assert args["with_debug"]


def test_parsing_topic_name():
    args = parse_arguments(["RHEL-7.6", "/var/www/html"])
    assert args["topic_name"] == "RHEL-7.6"


def test_parsing_1_variant():
    args = parse_arguments(["RHEL-8", "/var/www/html", "--variant", "BaseOs"])
    assert args["variants"] == ["BaseOs"]


def test_parsing_2_variants():
    args = parse_arguments(
        ["RHEL-8", "/var/www/html", "--variant", "BaseOs", "--variant", "AppStream"]
    )
    assert sorted(args["variants"]) == ["AppStream", "BaseOs"]


def test_parsing_1_arch():
    args = parse_arguments(["RHEL-8", "/var/www/html", "--arch", "ppc64le"])
    assert args["archs"] == ["ppc64le"]


def test_parsing_2_archs():
    args = parse_arguments(
        ["RHEL-8", "/var/www/html", "--arch", "x86_64", "--arch", "ppc64le"]
    )
    assert sorted(args["archs"]) == ["ppc64le", "x86_64"]


def test_parsing_combined_arguments():
    args = parse_arguments(
        [
            "RHEL-8.1",
            "/var/www/html",
            "--variant",
            "BaseOs",
            "--variant",
            "AppStream",
            "--arch",
            "x86_64",
        ]
    )
    assert args["topic_name"] == "RHEL-8.1"
    assert args["destination_folder"] == "/var/www/html"
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"]) == ["AppStream", "BaseOs"]
    assert not args["with_debug"]


def test_parsing_combined_arguments_different_order():
    args = parse_arguments(
        [
            "--variant",
            "BaseOs",
            "--arch",
            "x86_64",
            "--variant",
            "AppStream",
            "RHEL-8.1",
            "/home/dci/repo",
        ]
    )
    assert args["topic_name"] == "RHEL-8.1"
    assert args["destination_folder"] == "/home/dci/repo"
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"]) == ["AppStream", "BaseOs"]
    assert not args["with_debug"]


def test_parsing_combined_arguments_with_equals_signs():
    args = parse_arguments(
        [
            "--variant=BaseOs",
            "--arch=x86_64",
            "--variant=AppStream",
            "RHEL-8",
            "/tmp/repo",
        ]
    )
    assert args["topic_name"] == "RHEL-8"
    assert args["destination_folder"] == "/tmp/repo"
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"]) == ["AppStream", "BaseOs"]
    assert not args["with_debug"]
