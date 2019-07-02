import errno
import os
from tempfile import NamedTemporaryFile


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def delete_all_symlink_in_path(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                os.unlink(file_path)
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if os.path.islink(folder_path):
                os.unlink(folder_path)


def recreate_symlinks(symlinks, destination_path):
    for symlink in symlinks:
        link_path = os.path.join(destination_path, symlink["path"], symlink["name"])
        os.symlink(symlink["destination"], link_path)


def create_temp_file(content):
    cert = NamedTemporaryFile(delete=False)
    cert.write(content)
    cert.close()
    return cert


def build_destination_folder(topic, component):
    destination_folder = os.getenv("LOCAL_STORAGE_FOLDER")
    topic_name = topic["name"].strip().replace(" ", "_")
    component_type = component["type"].strip().replace(" ", "_").lower()
    return os.path.join(destination_folder, topic_name, component_type)
