"""
make text files for TBS 
make files with tables about footnotes, apostrophes, quotes, brackets, dashes, Words of JESUS, Names of the LORD, Quotes from the Old Testament in the NEW, 
sort changes table
"""

import os
from shutil import copy2 as copy_file

current_folder=os.path.dirname(os.path.abspath(__file__))
original_folder=os.path.join(current_folder, "Original")

paratext_folder=os.path.join(r'C:\My Paratext 9 Projects\BKS')
Bible_text_for_each_Book=dict()
for file_name in os.listdir(original_folder):
    original_file_path=os.path.join(original_folder,file_name)
    paratext_file_path=os.path.join(paratext_folder,file_name)
    copy_file(original_file_path,paratext_file_path)

    Book_name=file_name[2:5]
    with open(original_file_path,encoding='utf-8',mode='r') as file:
        lines=file.readlines()
    Bible_text_for_each_Book[Book_name]=lines

for Book_name in Bible_text_for_each_Book:
    Bible_text=Bible_text_for_each_Book[Book_name]
    print(Bible_text)