import os


def get_component_size(files_list):
    size = 0
    for file in files_list["files"]:
        size += file["size"]
    return size


def enough_space(files_list, local_path):
    component_size = get_component_size(files_list)
    st = os.statvfs(local_path)
    free_space = st.f_bavail * st.f_frsize * 1.05
    component_size_gb = component_size / 1024 / 1024 / 1024
    free_space_gb = free_space / 1024 / 1024 / 1024
    print("Component size %d GB" % component_size_gb)
    print("Free space %d GB" % free_space_gb)
    return component_size < free_space
