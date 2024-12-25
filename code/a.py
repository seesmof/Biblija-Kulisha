'''
wanting to extract all Words from the Ukrainian Bible Kulish 
'''

import os
import re
import string

from constants import constants as c

words=set()
for full_file_name in os.listdir(c.original_folder_path):
    file_path=os.path.join(c.original_folder_path,full_file_name)
    with open(file_path,encoding='utf-8',mode='r') as f:
        lines=f.readlines()

    # remove unnecessary tags
    tags_to_avoid=['mt','s','p','toc','h','id','c']
    lines=[line for line in lines if not any(f'\\{tag}' in line for tag in tags_to_avoid)]

    # remove formatting tags
    tags_to_remove=r'\\(\+*)(wj|qt|nd)(\s|\*)'
    lines=[re.sub(tags_to_remove,'',line) for line in lines]

    # remove verses
    verses_pattern=r'\\v\s\d+\s'
    lines=[re.sub(verses_pattern,'',line).strip() for line in lines]

    # remove footnotes
    footnote_pattern=r'\\(\+*)f(.*?)\\(\+*)f\*'
    lines=[re.sub(footnote_pattern,'',line).strip() for line in lines]

    # remove punctuation
    lines=[re.sub(r'[^\w\s\-]','',l) for l in lines]

    current_words=' '.join(lines)
    for word in current_words.split():
        words.add(word)
words=sorted(list(words))
print(words)