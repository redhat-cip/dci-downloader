import os
import tempfile
import shutil

from mock import patch

from dci_downloader.certificates import configure_ssl_certificates


@patch("dci_downloader.certificates.api.get_keys")
def test_configure_ssl_certificates_dont_call_api_refresh_key_if_cert_exists(
    get_keys_mock,
):
    with tempfile.NamedTemporaryFile() as tmpfile:
        settings = {"remoteci_id": "r1", "dci_cert_file": tmpfile.name}
        configure_ssl_certificates(settings)
        get_keys_mock.assert_not_called()


@patch(
    "dci_downloader.certificates.api.get_keys",
    return_value={"cert": "cert", "key": "key"},
)
def test_configure_ssl_certificates_call_api_refresh_key_if_cert_doesnt_exists(
    get_keys_mock,
):
    tmpdir = tempfile.mkdtemp()
    try:
        cert_file = os.path.join(tmpdir, "subfolder", "doesntexistyet.pem")
        settings = {
            "remoteci_id": "r1",
            "dci_cert_file": cert_file,
        }
        configure_ssl_certificates(settings)
        get_keys_mock.assert_called_once_with("r1")

        with open(cert_file) as f:
            assert f.read() == "key\ncert"
    finally:
        shutil.rmtree(tmpdir)
