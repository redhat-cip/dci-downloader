from pytest import raises
from dci_downloader.cli import parse_arguments


def test_parsing_no_options():
    args = parse_arguments(["RHEL-8", "/var/www/html"])
    assert args["name"] == "RHEL-8"
    assert args["archs"] == ["x86_64"]
    assert args["variants"] == []
    assert not args["with_debug"]
    assert not args["with_iso"]
    assert args["settings_file_paths"] is None
    assert args["download_folder"] == "/var/www/html"


def test_parsing_settings_file():
    args = parse_arguments(["--settings", "/etc/dci-downloader/settings.yml"])
    assert args["name"] is None
    assert args["archs"] == ["x86_64"]
    assert args["variants"] == []
    assert not args["with_debug"]
    assert not args["with_iso"]
    assert "/etc/dci-downloader/settings.yml" in args["settings_file_paths"]
    assert args["download_folder"] is None


def test_parsing_multiple_settings_file():
    args = parse_arguments([
        "--settings",
        "/etc/dci-downloader/settings.yml",
        "--settings",
        "/etc/dci-downloader/extra.yml",
    ])
    assert args["name"] is None
    assert args["archs"] == ["x86_64"]
    assert args["variants"] == []
    assert not args["with_debug"]
    assert not args["with_iso"]
    # ensure all settings files are present and in the right order
    assert args["settings_file_paths"] == [
        "/etc/dci-downloader/settings.yml",
        "/etc/dci-downloader/extra.yml"
    ]
    assert args["download_folder"] is None


def test_parsing_no_option_raise_exception():
    with raises(SystemExit):
        parse_arguments([])


def test_parsing_with_debug():
    args = parse_arguments(["RHEL-8", "/var/www/html", "--debug"])
    assert args["with_debug"]


def test_parsing_with_iso():
    args = parse_arguments(["RHEL-8", "/var/www/html", "--iso"])
    assert args["with_iso"]


def test_parsing_name():
    args = parse_arguments(["RHEL-7.6", "/var/www/html"])
    assert args["name"] == "RHEL-7.6"


def test_parsing_no_components():
    args = parse_arguments(["RHEL-8", "/var/www/"])
    assert args["component_id"] is None


def test_parsing_component_id():
    args = parse_arguments(
        [
            "RHEL-8",
            "/var/www/html",
            "--component-id",
            "27bbcd7d-021b-4f0a-b04e-e64f1be386f7",
        ]
    )
    assert args["name"] == "RHEL-8"
    assert args["download_folder"] == "/var/www/html"
    assert args["component_id"] == "27bbcd7d-021b-4f0a-b04e-e64f1be386f7"


def test_parsing_1_variant():
    args = parse_arguments(["RHEL-8", "/var/www/html", "--variant", "BaseOS"])
    assert args["variants"] == [{"name": "BaseOS", "with_debug": False, "with_iso": False}]


def test_parsing_2_variants():
    args = parse_arguments(
        ["RHEL-8", "/var/www/html", "--variant", "BaseOS", "--variant", "AppStream"]
    )
    assert sorted(args["variants"], key=lambda v: v["name"]) == [
        {"name": "AppStream", "with_debug": False, "with_iso": False},
        {"name": "BaseOS", "with_debug": False, "with_iso": False},
    ]


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
            "BaseOS",
            "--variant",
            "AppStream",
            "--arch",
            "ppc64le",
        ]
    )
    assert args["name"] == "RHEL-8.1"
    assert args["download_folder"] == "/var/www/html"
    assert args["archs"] == ["ppc64le"]
    assert sorted(args["variants"], key=lambda v: v["name"]) == [
        {"name": "AppStream", "with_debug": False, "with_iso": False},
        {"name": "BaseOS", "with_debug": False, "with_iso": False},
    ]
    assert not args["with_debug"]
    assert not args["with_iso"]


def test_parsing_combined_arguments_different_order():
    args = parse_arguments(
        [
            "--variant",
            "BaseOS",
            "--arch",
            "x86_64",
            "--variant",
            "AppStream",
            "RHEL-8.1",
            "/home/dci/repo",
        ]
    )
    assert args["name"] == "RHEL-8.1"
    assert args["download_folder"] == "/home/dci/repo"
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"], key=lambda v: v["name"]) == [
        {"name": "AppStream", "with_debug": False, "with_iso": False},
        {"name": "BaseOS", "with_debug": False, "with_iso": False},
    ]
    assert not args["with_debug"]
    assert not args["with_iso"]


def test_parsing_combined_arguments_with_equals_signs():
    args = parse_arguments(
        [
            "--variant=BaseOS",
            "--arch=x86_64",
            "--variant=AppStream",
            "RHEL-8",
            "/tmp/repo",
        ]
    )
    assert args["name"] == "RHEL-8"
    assert args["download_folder"] == "/tmp/repo"
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"], key=lambda v: v["name"]) == [
        {"name": "AppStream", "with_debug": False, "with_iso": False},
        {"name": "BaseOS", "with_debug": False, "with_iso": False},
    ]
    assert not args["with_debug"]
    assert not args["with_iso"]


def test_parsing_variants_with_debug():
    args = parse_arguments(
        [
            "--variant=BaseOS",
            "--arch=x86_64",
            "--variant=AppStream",
            "--debug",
            "RHEL-8",
            "/tmp/repo",
        ]
    )
    assert args["name"] == "RHEL-8"
    assert args["download_folder"] == "/tmp/repo"
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"], key=lambda v: v["name"]) == [
        {"name": "AppStream", "with_debug": True, "with_iso": False},
        {"name": "BaseOS", "with_debug": True, "with_iso": False},
    ]
    assert args["with_debug"]


def test_parsing_variants_with_iso():
    args = parse_arguments(
        [
            "--variant=BaseOS",
            "--arch=x86_64",
            "--variant=AppStream",
            "--iso",
            "RHEL-8",
            "/tmp/repo",
        ]
    )
    assert args["name"] == "RHEL-8"
    assert args["download_folder"] == "/tmp/repo"
    assert args["archs"] == ["x86_64"]
    assert sorted(args["variants"], key=lambda v: v["name"]) == [
        {"name": "AppStream", "with_debug": False, "with_iso": True},
        {"name": "BaseOS", "with_debug": False, "with_iso": True},
    ]
    assert args["with_iso"]
