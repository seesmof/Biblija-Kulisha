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
logs_folder_path=os.path.join(root,"logs")
paratext_folder_path=os.path.join("C:\\My Paratext 9 Projects\\BKS")

def copy_to_paratext():
    try:
        for full_file_name in os.listdir(original_folder_path):
            copy2(
                os.path.join(original_folder_path,full_file_name),
                os.path.join(paratext_folder_path,full_file_name)
            )
    except: 
        pass

def write_file(
    section:str,
    file_name:str,
    lines:list,
    root:str=root,
    tries:int=0
):
    # TODO remove this
    if tries>=3:
        fail(section,f"writing {file_name}")
        return
    try:
        target_file_path=os.path.join(root,file_name)
        with open(file=target_file_path,encoding='utf-8',mode='w') as f:
            f.writelines(lines)
    except:
        write_file(section,file_name,lines,root,tries+1)

def combine_lines(lines:list):
    # TODO figure out why this is here
    return [
        f'{line}\n' if line_index!=len(lines)-1 else line for line_index,line in enumerate(lines)
    ]

def remove_usfm_tags(line:str):
    return line.replace("\\wj*","").replace("\\wj ","").replace("\\+wj*","").replace("\\+wj ","").replace("\\nd*","").replace("\\nd ","").replace("\\+nd*","").replace("\\+nd ","").replace("\\qt*","").replace("\\qt ","").replace("\\+qt*","").replace("\\+qt ","")

def form_text_lined():
    def handle_quotes(verse:str):
        quote:bool=False
        words=[]
        for word in verse.split():
            if word=='\\qt' or word=='\\+qt': quote=True
            words.append(word.upper() if quote else word)
            if '\\qt*' in word or '\\+qt*' in word: quote=False
        return " ".join(words).replace("\\QT*","").replace("\\QT ","").replace("\\+QT*","").replace("\\+QT ","")

    def replace_plain_quotes_with_proper(verse:str):
        double_quotes="“ ”"
        double_open,double_close=double_quotes.split()
        # TODO add handling for nested quotes, try using stack somehow: JESUS THANK YOU LORD GOD ALMIGHTY HALLELUJAH AMEN
        single_quotes="‘ ’"
        single_open,single_close=single_quotes.split()

        opened:bool=False
        words=[]
        for word in verse.split():
            if '"' in word:
                opened=not opened
                words.append(word.replace('"',double_open if opened else double_close))
            else: 
                words.append(word)
        return " ".join(words)

    section="HUGE"
    global_lines=[]
    for full_file_name in os.listdir(original_folder_path):
        try:
            target_file_path=os.path.join(original_folder_path,full_file_name)
            with open(os.path.join(original_folder_path,full_file_name),encoding='utf-8',mode='r') as f:
                current_lines=f.readlines()
        except:
            fail(section,f"reading {full_file_name}")

        Book=current_lines[2].replace("\\h ","").strip()
        chapter=1
        for line in current_lines:
            if '\\c ' in line:
                chapter=line[3:].strip()
            elif '\\v ' in line:
                # remove verse tag
                verse=line[3:].strip()
                # remove WJ tags 
                verse=verse.replace("\\wj*","").replace("\\wj ","")
                # handle ND tags 
                verse="".join(
                    match.upper() 
                    if ' ' not in match 
                    else match 
                    for match in re.split(r'\\\+?nd (.*?)\\\+?nd\*',verse)
                )
                # handle QT tags
                verse=handle_quotes(verse)
                # handle Strong's numbers
                verse=re.sub(r'\|strong=\"[GH]\d{4}\"\\w\*',"",verse).replace("\\w ","")
                global_lines.append(f'{Book} {chapter}:{verse}')

    write_file(section,"Original.txt",combine_lines(global_lines))
    yes(section,"form file")

def form_logs():
    section="LOGS"

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

    write_file(section,"WJ.csv",combine_lines(WJ),logs_folder_path)
    write_file(section,"ND.csv",combine_lines(ND),logs_folder_path)
    write_file(section,"QT.csv",combine_lines(QT),logs_folder_path)
    write_file(section,"F.csv",combine_lines(F),logs_folder_path)
    yes(section,"form files")

def form_text_tbs():
    section="TEXT"
    for full_file_name in os.listdir(original_folder_path):
        target_file_path=os.path.join(original_folder_path,full_file_name)
        with open(file=target_file_path,encoding='utf-8',mode='r') as f:
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
            remove_usfm_tags(
                re.sub(
                    # Remove text from \f to \f*, which is any footnote
                    r'\\f(.*?)\\f\*','',line
                )
            )
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

        file_name,file_extension=full_file_name.split(".")
        # Remove number and BKS from filename
        # So `41MATBKS` will be `MAT`
        file_name=file_name[2:].replace("BKS","")
        # Change file extension and form full name
        file_extension="TXT"
        full_file_name=f'{file_name}.{file_extension}'

        write_file(section,full_file_name,lines,text_TBS_folder_path)
    yes(section,f"form files")

def form_text_solid():
    all_lines=[]
    for file_path in original_file_paths:
        with open(file_path,encoding='utf-8',mode='r') as filer:
            lines=filer.readlines()
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
    with open(os.path.join(text_solid_folder_path,'Solid.txt'),encoding='utf-8',mode='w') as filer:
        filer.write(res)

def perform_automations():
    copy_to_paratext()
    form_text_tbs()
    form_text_solid()
    form_logs()

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
