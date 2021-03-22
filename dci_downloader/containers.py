import re
import tempfile
import yaml

from subprocess import check_output, STDOUT, CalledProcessError

# from api import get_containers_list

DCI_CONTAINER_RE = re.compile(r"(?P<registry>.+?)/(?P<image>.+):(?P<tag>.+)")


def dci_image_info(dci_container):
    m = DCI_CONTAINER_RE.fullmatch(dci_container)
    return m.groupdict()


def dci_images_list_yaml_to_skopeo_format(
    images_list_yaml, registry_user, registry_password
):
    images_list = yaml.safe_load(images_list_yaml)
    skopeo_dict = {}
    for dci_container in images_list:
        image_info = dci_image_info(dci_container)
        if image_info["registry"] not in skopeo_dict:
            skopeo_dict[image_info["registry"]] = {
                "credentials": {
                    "username": registry_user,
                    "password": registry_password,
                },
                "images": {},
            }
        skopeo_dict[image_info["registry"]]["images"][image_info["image"]] = [
            image_info["tag"],
        ]

    return skopeo_dict


def skopeo_sync(skopeo_yaml_source, destination_registry):
    with tempfile.TemporaryFile() as tmpf:
        yaml.dump(skopeo_yaml_source, tmpf)
        tmpf.flush()
        skopeo_sync_command = [
            "skopeo",
            "sync",
            "--src",
            "yaml",
            "--dest",
            "docker",
            "--dest-tls-verify=false",
            "--dest-nocreds",
            tmpf,
            destination_registry,
        ]
        print("Running skopeo sync as: `%s`" % " ".join(skopeo_sync_command))
        try:
            output = check_output(skopeo_sync_command, stderr=STDOUT)
        except CalledProcessError as e:
            print(
                "Skopeo sync failed with return code: %d.\n"
                "Full command was: `%s`\n"
                "Output was:\n%s"
                % (e.returncode, " ".join(skopeo_sync_command), e.output)
            )
            raise e
        print("Skopeo sync succeeeded.\nOutput was:\n%s" % output)
