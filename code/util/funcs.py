import os
import re

from .consts import original_folder_path

def remove_footnotes_and_crossreferences_with_contents(verse: str):
    footnote_pattern=r'\\(\+*)(f|x)(.*?)\\(\+*)(f|x)\*'
    return re.sub(footnote_pattern,'',verse)

def remove_formatting_usfm_tags(verse: str):
    tags_pattern=r'\\(\+*)(wj|qt|nd|add|qs)(\s|\*)'
    return re.sub(tags_pattern,'',verse)

def remove_strongs_numbers(verse: str):
    strongs_number_closing_tag_pattern=r'\|strong=\"[GH]\d*?\"\\(\+?)w\*'
    verse=verse.replace('\\w ','').replace('\\+w ','')
    return re.sub(strongs_number_closing_tag_pattern,'',verse)

def remove_verse_tags_and_numbers(verse: str):
    verse_tag_and_number_pattern=r'\\v\s\d+\s'
    return re.sub(verse_tag_and_number_pattern,'',verse)

def get_ordered_Bible_Book_names(
    folder_path: str = original_folder_path,
):
    '''
    This function depends on the Original folder files being in the canonical Bible order, so please dont remove the 2-number prefixes from file names again!

    It return a list of Bible Book names as strings:
    - 01GEN
    - 02EXO
    - 03LEV
    - ...
    '''
    Book_names=[]
    for full_file_name in os.listdir(folder_path):
        # [2:] means remove the 2-number prefix
        file_name_without_extension=full_file_name[2:].split('.')[0]
        Book_names.append(file_name_without_extension)
    return Book_names

def read_file_lines(
    file_path:str
):
    with open(file_path,encoding='utf-8',mode='r') as f:
        return f.readlines()
    
def get_Book_name_from_full_file_name(
    file_name:str
):
    if 'usfm' not in file_name.lower(): 
        print(f'When trying to get Book name from file name: File format is not USFM for file named {file_name}')
        return 'ERROR Wrong file name'
    res=''
    if '-' in file_name: res = file_name[3:6]
    elif '.' in file_name: res = file_name[2:].split('.')[0]
    else: res = file_name[2:]
    return res