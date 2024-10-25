import os
from shutil import copy2

def get_relative_path(root_folder_path:str=os.path.dirname(os.path.abspath(__file__)),target_path:str=""):
    return os.path.join(root_folder_path,target_path)

ORIGINAL_FILES_PATH=get_relative_path("Original")
TEXT_FILES_PATH=get_relative_path("Text")
PARATEXT_PROJECT_PATH=get_relative_path("C:\\My Paratext 9 Projects\\BKS")

def copy_files_to_paratext_project():
    for file in os.listdir(ORIGINAL_FILES_PATH):
        copy2(
            get_relative_path(ORIGINAL_FILES_PATH,file),
            get_relative_path(PARATEXT_PROJECT_PATH,file)
        )
    print("All Bible original files copied to Paratext project")

copy_files_to_paratext_project()