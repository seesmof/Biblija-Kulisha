from calendar import c
import os
import re
import glob
import time
from shutil import copy2

root=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
original_folder_path=os.path.join(root,"Original")
original_file_paths=glob.glob(original_folder_path+"\\*.USFM")
output_folder_path=os.path.join(root,'Output')
text_TBS_folder_path=os.path.join(output_folder_path,'TXT TBS')
text_solid_folder_path=os.path.join(output_folder_path,'TXT SLD')
text_lined_folder_path=os.path.join(output_folder_path,'TXT LND')
logs_folder_path=os.path.join(root,"logs")
paratext_folder_path=os.path.join("C:\\My Paratext 9 Projects\\BKS")

def copy_to_paratext():
    try:
        for file_path in original_file_paths:
            copy2(
                file_path,
                os.path.join(paratext_folder_path,file_path.split('\\')[-1])
            )
    except: pass

def remove_usfm_tags(
    line:str
):
    tags_to_remove=[
        'wj',
        'nd',
        'qt',
    ]
    for tag in tags_to_remove:
        line=line.replace(f'\\{tag} ','').replace(f'\\{tag}*','')
        line=line.replace(f'\\+{tag} ','').replace(f'\\+{tag}*','')
    footnote_pattern=r'\\f(.*?)\\f\*'
    line=re.sub(footnote_pattern,'',line)
    return line

def form_logs():
    header='Book,Chapter,Verse,Content'
    WJ=[header]
    ND=[header]
    QT=[header]
    F=[header]

    for file_path in original_file_paths:
        with open(file_path,encoding='utf-8',mode='r') as f:
            lines=f.readlines()

        Book_name=lines[2].replace("\\h ","").strip()
        chapter_number=0

        for line in lines:
            if '\\c ' in line: 
                chapter_number=line[3:].strip()

            if '\\wj' in line or '\\+wj' in line:
                verse_number=re.findall(r'\\v\s\d+',line)[0][3:]
                contents=re.findall(r'\\\+?wj(.*?)\\\+?wj\*',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{remove_usfm_tags(c)}'
                    WJ.append(res)
            if '\\nd' in line or '\\+nd' in line:
                verse_number=re.findall(r'\\v\s\d+',line)[0][3:]
                contents=re.findall(r'\\\+?nd(.*?)\\\+?nd\*',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{remove_usfm_tags(c)}'
                    ND.append(res)
            if '\\qt' in line or '\\+qt' in line:
                verse_number=re.findall(r'\\v\s\d+',line)[0][3:]
                contents=re.findall(r'\\\+?qt(.*?)\\\+?qt\*',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{remove_usfm_tags(c)}'
                    QT.append(res)
            if '\\f' in line or '\\+f' in line:
                verse_number=re.findall(r'\\v\s\d+',line)[0][3:]
                contents=re.findall(r'\\\+?ft\s(.*?)\\\+?f\*',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{c}'
                    F.append(res)

    try:
        with open(os.path.join(logs_folder_path,'WJ.csv'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(WJ))
    except: pass

    try:
        with open(os.path.join(logs_folder_path,'ND.csv'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(ND))
    except: pass

    try:
        with open(os.path.join(logs_folder_path,'QT.csv'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(QT))
    except: pass

    try:
        with open(os.path.join(logs_folder_path,'F.csv'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(F))
    except: pass

def form_text_tbs():
    for file_path in original_file_paths:
        with open(file_path,encoding='utf-8',mode='r') as f:
            lines=f.readlines()

        lines=[
            line for line in lines 
            # Remove `\ide`
            if '\\ide' not in line 
            # Remove `\h`
            and '\\h' not in line 
            # Remove `\toc3`
            and '\\toc3' not in line 
            # Remove `\mt1`
            and '\\mt1' not in line 
            # Remove `\p`
            and '\\p' not in line
        ]
        lines=[
            remove_usfm_tags(line)
            # Remove ` - Biblija Kulisha Standartna`
            .replace(" - Biblija Kulisha Standartna","")
            # Change `\id ` to `###`
            .replace("\\id ","###")
            # Change `\toc1 ` to `###!!`
            .replace("\\toc1","###!!")
            # Change `\toc2 ` to `###!`
            .replace("\\toc2","###!")
            # Change `\c ` to `##`
            .replace("\\c ","##")
            # Change `\v ` to `#`
            .replace("\\v ","#")
            # Replace `[ ]` with `* *`
            .replace("[","*").replace("]",'*') 
            for line in lines
        ]
        lines=[
            # Put chapter number lines on a separate line
            line[:-2]+'\n' if re.search(r'##\d+\s',line) 
            # If its not a chapter number, then write it as it is
            else line 
            for line in lines
        ]

        file_name,file_extension=file_path.split('\\')[-1].split(".")
        # Remove number and BKS from filename
        # So `41MATBKS` will be `MAT`
        file_name=file_name[2:].replace("BKS","")
        # Change file extension and form full name
        file_extension="TXT"
        full_name=f'{file_name}.{file_extension}'

        try:
            with open(os.path.join(text_TBS_folder_path,full_name),encoding='utf-8',mode='w') as f:
                f.writelines(lines)
        except: pass

def form_text_solid():
    all_lines=[]
    for file_path in original_file_paths:
        with open(file_path,encoding='utf-8',mode='r') as f:
            lines=f.readlines()
        lines=[
            remove_usfm_tags(
                # Match verse tags and numbers and remove them
                re.sub(r'\\v\s\d+\s','',line)
            )
            for line in lines
            if '\\p' not in line
            and '\\c' not in line
            and '\\id' not in line
            and '\\h' not in line
            and '\\toc1' not in line
            and '\\toc2' not in line
            and '\\toc3' not in line
            and '\\mt1' not in line
        ]
        all_lines+=lines
    # Join everything into one solid wall of text, ALLELUJAH JESUS THANK YOU LORD GOD ALMIGHTY!
    res=" ".join(
        # Replace all new line tags
        [line.replace('\n','') for line in all_lines]
    )
    try:
        with open(os.path.join(text_solid_folder_path,'Solid.txt'),encoding='utf-8',mode='w') as f:
            f.write(res)
    except: pass

def form_text_lined():
    gls=[]
    for fp in original_file_paths:
        with open(fp,encoding='utf-8',mode='r') as f:
            ls=f.readlines()
        bn=ls[2][3:].strip()
        cn=1
        for l in ls:
            if '\\p' in l or '\\id' in l or '\\h' in l or '\\toc1' in l or '\\toc2' in l or '\\toc3' in l or '\\mt1' in l:
                continue
            elif '\\c ' in l:
                cn=l[3:].split()[0]
                continue
            v=l[3:].strip()
            r=f'{bn} {cn}:{remove_usfm_tags(re.sub(r'\\v\s\d+\s','',v))}'
            gls.append(r)
    try:
        with open(os.path.join(text_lined_folder_path,'Lined.txt'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(gls))
    except: pass

def perform_automations():
    print()
    copy_to_paratext()
    print('Copied Bible files to Paratext')
    form_text_tbs()
    print('Formed TBS Bible text file')
    form_text_solid()
    print('Formed solid Bible text file')
    form_text_lined()
    print('Formed lined Bible text file')
    form_logs()
    print('Formed log files')

def monitor_files_for_changes():
    latest_file=max(original_file_paths,key=os.path.getmtime)
    last_modification_time=os.path.getmtime(latest_file)
    perform_automations()
    while 1:
        latest_file=max(original_file_paths,key=os.path.getmtime)
        current_modification_time=os.path.getmtime(latest_file)
        if last_modification_time!=current_modification_time:
            perform_automations()
            last_modification_time=current_modification_time
        time.sleep(1)

if __name__=="__main__":
    monitor_files_for_changes()
