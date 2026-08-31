import os
from Original_Automations import form_text_lined

paratext_project_folder_path: str = os.path.join("C:\\My Paratext 9 Projects\\UFB")
output_file_path: str = os.path.join(
    "C:\\work\\Biblija-Kulisha\\docs\\Revision", "Lined.txt"
)

form_text_lined(
    paratext_project_folder_path,
    vault_output_file_path=None,
    local_output_file_path=output_file_path,
)
