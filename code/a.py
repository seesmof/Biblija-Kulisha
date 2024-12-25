import os
import re

from Automations import original_folder

texts=dict()
for full_file_name in os.listdir(original_folder):
    file_path=os.path.join(original_folder,full_file_name)
    with open(file_path,encoding='utf-8',mode='r') as f:
        text=f.read()
