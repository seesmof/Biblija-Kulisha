import os
import re

from .consts import original_folder_path

def remove_footnotes_with_text(verse: str):
    footnote_pattern=r'\\(\+*)f(.*?)\\(\+*)f\*'
    return re.sub(footnote_pattern,'',verse)

def remove_formatting_usfm_tags(verse: str):
    tags_pattern=r'\\(\+*)(wj|qt|nd)(\s|\*)'
    return re.sub(tags_pattern,'',verse)

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
        file_name_without_extension=full_file_name.split('.')[0]
        Book_names.append(file_name_without_extension)
    return Book_names