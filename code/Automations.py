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

def remove_usfm_tags(line:str):
    # Remove WJ, ND, QT tags from the Bible verse line
    tags_to_remove=[
        'wj',
        'nd',
        'qt',
    ]
    for tag in tags_to_remove:
        line=line.replace(f'\\{tag} ','').replace(f'\\{tag}*','')
        # Replace those if they are indented as well
        # + sign marks an indented tag in USFM (a tag that is inside another tag)
        #   for example: when JESUS quotes from the Old Testament:
        #   Words of JESUS will be in \WJ and the quote will be in \QT
        line=line.replace(f'\\+{tag} ','').replace(f'\\+{tag}*','')

    # Footnotes begin with \f and ends with \f* always
    # Everything that is inbetween is selected also
    footnote_pattern=r'\\f(.*?)\\f\*'
    line=re.sub(footnote_pattern,'',line)
    return line

def form_logs():
    def get_verse_number(line:str) -> int:
        verse_number_pattern=r'\\v\s\d+'
        # Look for verses inside the line 
        found_verses=re.findall(verse_number_pattern,line)
        # Select first match because verse is usually at the beginning of the line 
        verse=found_verses[0]
        # Strip the '\v ' text from it
        verse_number=verse[3:]
        # And return the number as integer
        return int(verse_number)

    header='Book,Chapter,Verse,Content'
    WJ=[header]
    ND=[header]
    QT=[header]
    F=[header]
    Quotes=[header]
    Apostrophes=[header]
    Dashes=[header]

    for file_path in original_file_paths:
        with open(file_path,encoding='utf-8',mode='r') as f:
            lines=f.readlines()

        Book_name=lines[2].replace("\\h ","").strip()
        chapter_number=0

        for line in lines:
            if '\\c ' in line: 
                chapter_number=line[3:].strip()

            if '\\wj' in line or '\\+wj' in line:
                verse_number=get_verse_number(line)
                contents=re.findall(r'\\\+?wj(.*?)\\\+?wj\*',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{remove_usfm_tags(c)}'
                    WJ.append(res)
            if '\\nd' in line or '\\+nd' in line:
                verse_number=get_verse_number(line)
                contents=re.findall(r'\\\+?nd(.*?)\\\+?nd\*',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{remove_usfm_tags(c)}'
                    ND.append(res)
            if '\\qt' in line or '\\+qt' in line:
                verse_number=get_verse_number(line)
                contents=re.findall(r'\\\+?qt(.*?)\\\+?qt\*',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{remove_usfm_tags(c)}'
                    QT.append(res)
            if '\\f' in line or '\\+f' in line:
                verse_number=get_verse_number(line)
                contents=re.findall(r'\\\+?ft\s(.*?)\\\+?f\*',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{c}'
                    F.append(res)
            if '„' in line or '‟' in line:
                verse_number=get_verse_number(line)
                contents=[w for w in line.split() if '„' in w or '‟' in w]
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{c}'
                    Quotes.append(res)
            if 'ʼ' in line:
                verse_number=get_verse_number(line)
                contents=[w for w in line.split() if 'ʼ' in w]
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{c}'
                    Apostrophes.append(res)
            if '—' in line:
                verse_number=get_verse_number(line)
                contents=re.findall(r'\w+\s*—|\W\s*—',line)
                for c in contents:
                    res=f'{Book_name},{chapter_number},{verse_number},{c}'
                    Dashes.append(res)

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

    try:
        with open(os.path.join(logs_folder_path,'Quotes.csv'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(Quotes))
    except: pass

    try:
        with open(os.path.join(logs_folder_path,'Apostrophes.csv'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(Apostrophes))
    except: pass

    try:
        with open(os.path.join(logs_folder_path,'Dashes.csv'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(Dashes))
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
            line
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
            # Remove USFM formatting tags
            .replace('\\wj ','').replace('\\wj*','').replace('\\+wj ','').replace('\\+wj*','')
            .replace('\\nd ','').replace('\\nd*','').replace('\\+nd ','').replace('\\+nd*','')
            .replace('\\qt ','').replace('\\qt*','').replace('\\+qt ','').replace('\\+qt*','')
            for line in lines
        ]
        lines=[
            # Put chapter number lines on a separate line
            line[:-2]+'\n' if re.search(r'##\d+\s',line) 
            # If its not a chapter number, then write it as it is
            else line 
            for line in lines
        ]
        lines=[
            re.sub(r'\\f\s\+\s\\fr\s\d+\:\d+\s\\ft\s','[',line).replace('\\f*',']')
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
    avoid_these=[
        'p',
        'id',
        'h',
        'mt1',
        'toc1',
        'toc2',
        'toc3',
    ]
    all_lines=[]
    for file_path in original_file_paths:
        with open(file_path,encoding='utf-8',mode='r') as f:
            lines=f.readlines()
        Book_name=lines[2][3:].strip()
        chapter_number=1
        for line in lines:
            if any(tag in line for tag in avoid_these): continue
            if '\\c ' in line:
                chapter_number=line[3:].split()[0]
                continue
            # Remove the `\v ` tag from line
            verse_text=line[3:].strip()
            line=f'{Book_name} {chapter_number}:{remove_usfm_tags(verse_text)}'
            all_lines.append(line)
    try:
        with open(os.path.join(text_lined_folder_path,'Lined.txt'),encoding='utf-8',mode='w') as f:
            f.write('\n'.join(all_lines))
    except: pass

def perform_automations():
    print()
    copy_to_paratext()
    print('Copied Bible files to Paratext')
    form_text_tbs()
    print('Formed TBS Bible text files')
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
