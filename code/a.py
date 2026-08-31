import os

paratext_project_folder_path: str = os.path.join("C:\\My Paratext 9 Projects\\UFB")

for file_name in os.listdir(paratext_project_folder_path):
    if ".usfm" not in file_name.lower() or ".bak" in file_name.lower():
        continue
