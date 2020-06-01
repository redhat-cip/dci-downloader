import os
import tempfile
import shutil

from mock import patch

from dci_downloader.certificates import configure_ssl_certificates


@patch(
    "dci_downloader.certificates.api.cert_is_valid", return_value=True,
)
@patch("dci_downloader.certificates.api.get_keys")
def test_configure_ssl_certificates_dont_call_api_refresh_key_if_certs_exist(
    get_keys_mock, cert_is_valid_mock
):
    with tempfile.NamedTemporaryFile() as key_file, tempfile.NamedTemporaryFile() as cert_file:
        settings = {
            "remoteci_id": "r1",
            "dci_key_file": key_file.name,
            "dci_cert_file": cert_file.name,
        }
        configure_ssl_certificates(settings)
        get_keys_mock.assert_not_called()


@patch(
    "dci_downloader.certificates.api.get_keys",
    return_value={"cert": "cert", "key": "key"},
)
def test_configure_ssl_certificates_call_api_refresh_key_if_certs_dont_exist(
    get_keys_mock,
):
    tmpdir = tempfile.mkdtemp()
    try:
        key_file = os.path.join(tmpdir, "subfolder", "dci.key")
        cert_file = os.path.join(tmpdir, "subfolder", "dci.crt")
        settings = {
            "remoteci_id": "r1",
            "dci_key_file": key_file,
            "dci_cert_file": cert_file,
        }
        configure_ssl_certificates(settings)
        get_keys_mock.assert_called_once_with("r1")

        with open(cert_file) as f:
            assert f.read() == "cert"
        with open(key_file) as f:
            assert f.read() == "key"
    finally:
        shutil.rmtree(tmpdir)
