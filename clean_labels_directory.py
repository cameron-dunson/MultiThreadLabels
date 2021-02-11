import os

project_dir = os.path.dirname(os.path.abspath(__file__))


def clean_dir(directory: str = "") -> str:
    if directory == "":
        working_dir = project_dir + f"/{directory}"
    else:
        working_dir = project_dir + f"/{directory}/"
    dir_contents = os.listdir(working_dir)
    for k in dir_contents:
        file_to_remove = working_dir + f"{k}"
        os.remove(file_to_remove)
        print(f"Removed Resource: {file_to_remove}")
    print("DONE")
    return "DONE"


def clean_labels_sub_directories(directory: str) -> str:
    sub_dir = project_dir + f"/{directory}/"
    sub_dir_list = os.listdir(sub_dir)
    for directory in sub_dir_list:
        sub_dir_labels = sub_dir + directory
        sub_dir_files = os.listdir(sub_dir_labels)
        for n in sub_dir_files:
            file_to_remove = sub_dir_labels + f"/{n}"
            os.remove(file_to_remove)
            print(f"Removed File: {file_to_remove}")
    print("DONE")
    return "DONE"


clean_labels_sub_directories("labels")
