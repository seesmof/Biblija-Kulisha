import os
from shutil import copy2
import re

def get_relative_path(root_folder_path:str=os.path.dirname(os.path.abspath(__file__)),target_path:str=""):
    return os.path.join(root_folder_path,target_path)

ORIGINAL_FILES_PATH=get_relative_path("Original")
TEXT_FILES_PATH=get_relative_path("Text")
PARATEXT_PROJECT_PATH=get_relative_path("C:\\My Paratext 9 Projects\\BKS")

def copy_original_to_paratext():
    for file in os.listdir(ORIGINAL_FILES_PATH):
        copy2(
            get_relative_path(ORIGINAL_FILES_PATH,file),
            get_relative_path(PARATEXT_PROJECT_PATH,file)
        )

# copy_original_to_paratext()

def copy_original_to_text():
    for file in os.listdir(ORIGINAL_FILES_PATH):
        with open(get_relative_path(ORIGINAL_FILES_PATH,file), mode='r',encoding='utf-8') as f:
            lines=f.readlines()
        lines=[
            line for line in lines 
            if '\\ide' not in line 
            and '\\h' not in line 
            and '\\toc3' not in line 
            and '\\mt1' not in line 
            and '\\p' not in line
        ]
        lines=[
            line
            .replace(" - Biblija Kulisha Standartna","")
            .replace("\\id ","###")
            .replace("\\toc1","###!!")
            .replace("\\toc2","###!")
            .replace("\\c ","##")
            .replace("\\v ","#")
            .replace("\\wj*","").replace("\\wj ","")
            .replace("\\nd*","").replace("\\nd ","")
            .replace("\\qt*","").replace("\\qt ","")
            .replace("[","*")
            .replace("]",'*') 
            for line in lines
        ]
        lines=[
            line[:-2]+'\n' if re.search(r'##\d+\s',line) 
            else line 
            for line in lines
        ]

        file_name,file_extension=file.split(".")
        file_name=file_name[2:].replace("BKS","")
        file_extension="TXT"
        file=f'{file_name}.{file_extension}'

        with open(get_relative_path(TEXT_FILES_PATH,file),encoding='utf-8',mode='w') as f:
            f.writelines(lines)

# copy_original_to_text()

def make_single_text_file():
    global_lines=[]
    for file in os.listdir(ORIGINAL_FILES_PATH):
        with open(get_relative_path(ORIGINAL_FILES_PATH,file),mode='r',encoding='utf-8') as f:
            current_lines=f.readlines()
            Book=current_lines[2].replace("\\h ","").strip()
            chapter=1
            for line in current_lines:
                if '\\c ' in line:
                    chapter=line[3:].strip()
                elif '\\v ' in line:
                    verse=line[3:].strip()
                    global_lines.append(f'{Book} {chapter}:{verse}')
    with open(get_relative_path(target_path='Original.txt'),mode='w',encoding='utf-8') as f:
        f.writelines([
            line+'\n' if index!=len(global_lines)-1 
            else line 
            for index,line in enumerate(global_lines)
        ])

make_single_text_file()