import os
import re
import glob
import time
from shutil import copy2

ROOT_PATH=os.path.dirname(os.path.abspath(__file__))
ORIGINAL_FILES_PATH=os.path.join(ROOT_PATH,"Original")
ORIGINAL_FILES=ORIGINAL_FILES_PATH+"\\*.USFM"
TEXT_FILES_PATH=os.path.join(ROOT_PATH,"Text")
PARATEXT_PROJECT_PATH=os.path.join("C:\\My Paratext 9 Projects\\BKS")

def copy_original_to_paratext():
    for full_file_name in os.listdir(ORIGINAL_FILES_PATH):
        copy2(
            os.path.join(ORIGINAL_FILES_PATH,full_file_name),
            os.path.join(PARATEXT_PROJECT_PATH,full_file_name)
        )

def copy_original_to_text():
    for full_file_name in os.listdir(ORIGINAL_FILES_PATH):
        with open(os.path.join(ORIGINAL_FILES_PATH,full_file_name), mode='r',encoding='utf-8') as f:
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

        file_name,file_extension=full_file_name.split(".")
        file_name=file_name[2:].replace("BKS","")
        file_extension="TXT"
        full_file_name=f'{file_name}.{file_extension}'

        with open(os.path.join(TEXT_FILES_PATH,full_file_name),encoding='utf-8',mode='w') as f:
            f.writelines(lines)

def make_single_text_file():
    def handle_quotes(verse:str):
        quote:bool=False
        words=[]
        for word in verse.split():
            if word=='\\qt': quote=True
            words.append(word.upper() if quote else word)
            if '\\qt*' in word: quote=False
        return " ".join(words).replace("\\QT*","").replace("\\QT ","")
    global_lines=[]
    for full_file_name in os.listdir(ORIGINAL_FILES_PATH):
        with open(os.path.join(ORIGINAL_FILES_PATH,full_file_name),mode='r',encoding='utf-8') as f:
            current_lines=f.readlines()
            Book=current_lines[2].replace("\\h ","").strip()
            chapter=1
            for line in current_lines:
                if '\\c ' in line:
                    chapter=line[3:].strip()
                elif '\\v ' in line:
                    # remove verse tag
                    verse=line[3:].strip()
                    # remove WJ tags 
                    verse=verse.replace("\\wj*","").replace("\\wj ","")
                    # handle ND tags 
                    verse="".join(m.upper() if ' ' not in m else m for m in re.split(r'\\nd (.*?)\\nd\*',verse))
                    # handle QT tags
                    verse=handle_quotes(verse)
                    # handle Strong's numbers
                    verse=re.sub(r'\|strong=\"[GH]\d{4}\"\\w\*',"",verse).replace("\\w ","")
                    global_lines.append(f'{Book} {chapter}:{verse}')
    with open(os.path.join(ROOT_PATH,'Original.txt'),mode='w',encoding='utf-8') as f:
        f.writelines([
            line+'\n' if index!=len(global_lines)-1 
            else line 
            for index,line in enumerate(global_lines)
        ])

def perform_automations():
    copy_original_to_paratext()
    # copy_original_to_text()
    make_single_text_file()

def monitor_files_for_changes():
    def get_last_modified_file():
        return max(glob.glob(ORIGINAL_FILES),key=os.path.getmtime)
    def get_modification_time(file:str):
        return os.path.getmtime(file)

    latest_file=get_last_modified_file()
    last_modification_time=get_modification_time(latest_file)
    while 1:
        latest_file=get_last_modified_file()
        current_modification_time=get_modification_time(latest_file)
        if last_modification_time!=current_modification_time:
            perform_automations()
            last_modification_time=current_modification_time
            print(latest_file.split("\\")[-1][2:5],time.ctime(last_modification_time))
        time.sleep(1)

monitor_files_for_changes()