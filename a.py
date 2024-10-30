# automatically log JESUS' Words into a text file with ranges

import os 
import glob 
root=os.path.dirname(os.path.abspath(__file__))
original=os.path.join(root,"Original")
Bible_text_files=glob.glob(original+"\\*.USFM")

for file_path in Bible_text_files:
    with open(file_path,encoding="utf-8") as f:
        lines=f.readlines()
    Book_name=lines[2].replace("\\h ","").strip()
    last_chapter=0
    for line in lines:
        if '\\c ' in line:
            last_chapter=line[3:].strip()
        if 'wj' in line:
            print(Book_name,last_chapter,line[3:].split()[0])