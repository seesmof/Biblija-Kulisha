import shutil
import time
import util
import os
import re

'''
copy Original and Revision files to their paratext projects 
    strip all rem tags
make a TBS text version of the Original
'''

def copy_files_to_paratext_project(
    project_abbreviation: str = 'UBK', 
    local_files_folder_path: str = util.original_folder_path,
    remove_comenting_rem_tags: bool = False,
):
    paratext_project_folder_path=os.path.join(util.paratext_projects_folder_path,project_abbreviation)
    for file_name in os.listdir(local_files_folder_path):
        paratext_file_path=os.path.join(paratext_project_folder_path,file_name)
        local_file_path=os.path.join(local_files_folder_path,file_name)
        shutil.copy2(local_file_path,paratext_file_path)

        if remove_comenting_rem_tags:
            with open(paratext_file_path,encoding='utf-8',mode='r') as f:
                lines=f.readlines()
            lines=[l for l in lines if not l.startswith(r'\rem ')]
            with open(paratext_file_path,encoding='utf-8',mode='w') as f:
                f.write('\n'.join([l.strip() for l in lines]))


def make_tbs_text_files(
    folder_path:str=util.original_folder_path,
):
    for file_name in os.listdir(folder_path):
        Book_name=file_name[2:].replace('.USFM','')
        file_path=os.path.join(folder_path,file_name)
        with open(file_path,encoding='utf-8',mode='r') as f:
            lines=f.readlines()

        needed_tags=['toc','v','s','c']
        lines=[f'###{Book_name}']+[
            re.sub(r'\\f\s\+\s\\ft\s','[',line).replace(r'\f*',']')
            .replace(r'\v ','#')
            .replace(r'\c ','##')
            .replace(r'\toc2','###!')
            .replace(r'\toc1','###!!')
            for line in lines 
            if any(tag in line for tag in needed_tags)
        ]
    
        output_file_path=os.path.join(util.docs_folder_path,'Original','TBS',file_name[2:].replace('USFM','TXT'))
        with open(output_file_path,encoding='utf-8',mode='w') as f:
            f.write('\n'.join([l.strip() for l in lines]))



def perform_automations():
    print('Copy Original files to Paratext')
    copy_files_to_paratext_project()
    print('Copy Revision files to Paratext')
    copy_files_to_paratext_project('UFB',util.revision_folder_path,True)
    print('Form TBS text files')
    make_tbs_text_files()


def watch_folder_for_changes(
    folder_path:str=util.original_folder_path,
):
    file_paths=[os.path.join(folder_path,file_name) for file_name in os.listdir(folder_path)]
    last_modified_file = max(file_paths, key=os.path.getmtime)
    last_modification_time = os.path.getmtime(last_modified_file)
    perform_automations()
    while 1:
        last_modified_file = max(file_paths, key=os.path.getmtime)
        current_modification_time = os.path.getmtime(last_modified_file)
        if last_modification_time != current_modification_time:
            perform_automations()
            last_modification_time = current_modification_time
        time.sleep(1)

if __name__ == "__main__":
    watch_folder_for_changes()