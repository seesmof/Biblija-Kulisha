import util
import os
import re

def make_solid_file(
    source_folder_path = util.original_folder_path,
    vault_output_file_path = r'E:\Notatnyk\Біблія Куліша.log',
):
    output=[]
    for file_name in os.listdir(source_folder_path):
        if 'FRT' in file_name: continue
        res=[]
        file_path=os.path.join(source_folder_path,file_name)
        lines=util.read_file_lines(file_path)
        avoided_tags='h,toc,c,p,id,mt,s'
        avoided_tags=avoided_tags.split(',')
        cleared_lines=[l for l in lines if not any(t in l for t in avoided_tags)]
        for l in cleared_lines:
            v,c=l[3:].split(' ',maxsplit=1)
            res.append(c.strip())
        res=' '.join(res)
        output.append(res)
    output=' '.join(output)
        
    try:
        if 'Notatnyk' not in vault_output_file_path:
            vault_output_file_path=os.path.join(r'E:\Notatnyk',vault_output_file_path)
        with open(vault_output_file_path,encoding='utf-8',mode='w') as f:
            f.write(output.strip())
    except: pass

make_solid_file(source_folder_path=util.original_folder_path,vault_output_file_path=r'E:\Notatnyk\Біблія Куліша.log')
print('Solid Original')