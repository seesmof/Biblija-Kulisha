from code.consts import constants as c
from Automations import remove_usfm_tags

import os 

for f in os.listdir(c.original_folder_path):
    Bn=f[2:5]
    fp=os.path.join(c.original_folder_path,f)
    with open(fp,encoding='utf-8',mode='r') as f:
        ls=f.readlines()
    for l in ls:
        l=remove_usfm_tags(l).strip()
        print(l,l[-1])