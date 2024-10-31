import os
import re
import glob
import time
from shutil import copy2

ROOT_PATH=os.path.dirname(os.path.abspath(__file__))
ORIGINAL_FILES_PATH=os.path.join(ROOT_PATH,"Original")
ORIGINAL_FILES=glob.glob(ORIGINAL_FILES_PATH+"\\*.USFM")
TEXT_FILES_PATH=os.path.join(ROOT_PATH,"Text")
PARATEXT_PROJECT_PATH=os.path.join("C:\\My Paratext 9 Projects\\BKS")

def copy_original_to_paratext():
    for full_file_name in os.listdir(ORIGINAL_FILES_PATH):
        copy2(
            os.path.join(ORIGINAL_FILES_PATH,full_file_name),
            os.path.join(PARATEXT_PROJECT_PATH,full_file_name)
        )

def copy_original_to_text():
    for full_file_name in os.listdir(ORIGINAL_FILES_PATH):
        with open(os.path.join(ORIGINAL_FILES_PATH,full_file_name), mode='r',encoding='utf-8') as f:
            lines=f.readlines()
        lines=[
            line for line in lines 
            if '\\ide' not in line 
            and '\\h' not in line 
            and '\\toc3' not in line 
            and '\\mt1' not in line 
            and '\\p' not in line
        ]
        lines=[
            line
            .replace(" - Biblija Kulisha Standartna","")
            .replace("\\id ","###")
            .replace("\\toc1","###!!")
            .replace("\\toc2","###!")
            .replace("\\c ","##")
            .replace("\\v ","#")
            .replace("\\wj*","").replace("\\wj ","")
            .replace("\\nd*","").replace("\\nd ","")
            .replace("\\qt*","").replace("\\qt ","")
            .replace("[","*")
            .replace("]",'*') 
            for line in lines
        ]
        lines=[
            line[:-2]+'\n' if re.search(r'##\d+\s',line) 
            else line 
            for line in lines
        ]

        file_name,file_extension=full_file_name.split(".")
        file_name=file_name[2:].replace("BKS","")
        file_extension="TXT"
        full_file_name=f'{file_name}.{file_extension}'

        with open(os.path.join(TEXT_FILES_PATH,full_file_name),encoding='utf-8',mode='w') as f:
            f.writelines(lines)

def make_single_text_file():
    def handle_quotes(verse:str):
        quote:bool=False
        words=[]
        for word in verse.split():
            if word=='\\qt': quote=True
            words.append(word.upper() if quote else word)
            if '\\qt*' in word: quote=False
        return " ".join(words).replace("\\QT*","").replace("\\QT ","")
    global_lines=[]
    for full_file_name in os.listdir(ORIGINAL_FILES_PATH):
        with open(os.path.join(ORIGINAL_FILES_PATH,full_file_name),mode='r',encoding='utf-8') as f:
            current_lines=f.readlines()
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
                    verse="".join(m.upper() if ' ' not in m else m for m in re.split(r'\\nd (.*?)\\nd\*',verse))
                    # handle QT tags
                    verse=handle_quotes(verse)
                    # handle Strong's numbers
                    verse=re.sub(r'\|strong=\"[GH]\d{4}\"\\w\*',"",verse).replace("\\w ","")
                    global_lines.append(f'{Book} {chapter}:{verse}')
    with open(file=os.path.join(ROOT_PATH,"Original.txt"),encoding='utf-8',mode='w') as f:
        f.writelines([
            line+'\n' if index!=len(global_lines)-1 
            else line 
            for index,line in enumerate(global_lines)
        ])

def form_log_files():
    DEFAULT = '\033[0m'; BOLD = '\033[1m';ITALIC = '\033[3m';UNDERLINE = '\033[4m';UNDERLINE_THICK = '\033[21m';HIGHLIGHTED = '\033[7m';HIGHLIGHTED_BLACK = '\033[40m';HIGHLIGHTED_RED = '\033[41m';HIGHLIGHTED_GREEN = '\033[42m';HIGHLIGHTED_YELLOW = '\033[43m';HIGHLIGHTED_BLUE = '\033[44m';HIGHLIGHTED_PURPLE = '\033[45m';HIGHLIGHTED_CYAN = '\033[46m';HIGHLIGHTED_GREY = '\033[47m';HIGHLIGHTED_GREY_LIGHT = '\033[100m';HIGHLIGHTED_RED_LIGHT = '\033[101m';HIGHLIGHTED_GREEN_LIGHT = '\033[102m';HIGHLIGHTED_YELLOW_LIGHT = '\033[103m';HIGHLIGHTED_BLUE_LIGHT = '\033[104m';HIGHLIGHTED_PURPLE_LIGHT = '\033[105m';HIGHLIGHTED_CYAN_LIGHT = '\033[106m';HIGHLIGHTED_WHITE_LIGHT = '\033[107m';STRIKE_THROUGH = '\033[9m';MARGIN_1 = '\033[51m';MARGIN_2 = '\033[52m';BLACK = '\033[30m';RED_DARK = '\033[31m';GREEN_DARK = '\033[32m';YELLOW_DARK = '\033[33m';BLUE_DARK = '\033[34m';PURPLE_DARK = '\033[35m';CYAN_DARK = '\033[36m';GREY_DARK = '\033[37m';BLACK_LIGHT = '\033[90m';RED = '\033[91m';GREEN = '\033[92m';YELLOW = '\033[93m';BLUE = '\033[94m';PURPLE = '\033[95m';CYAN = '\033[96m';WHITE = '\033[97m';echo = lambda values, color: print("%s%s%s" % (color, values, DEFAULT)) if color else print("%s%s" % (values, DEFAULT)) # source: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal#:~:text=%2C%20color%3DCYAN)-,1%20Line,-Simply%20copy%20paste
    JESUS_Words=[]
    LORD_Names=[]
    OT_Quotes=[]
    for file_path in ORIGINAL_FILES:
        with open(file_path,encoding='utf-8',mode='r') as f:
            lines=f.readlines()
        Book_name=lines[2].replace("\\h ","").strip()
        last_chapter=0
        for line in lines:
            if '\\c ' in line: 
                last_chapter=line[3:].strip()
            if '\\wj' in line:
                verse_reference=f"{Book_name} {last_chapter}:{line[3:].split()[0]}"
                if '*' not in line: 
                    echo(f"WARNING: Missing closing tag {verse_reference}",color=RED_DARK)
                    exit()
                JESUS_Words.append(verse_reference)
            if '\\nd' in line:
                verse_reference=f"{Book_name} {last_chapter}:{line[3:].split()[0]}"
                if '*' not in line: 
                    echo(f"WARNING: Missing closing tag {verse_reference}",color=RED_DARK)
                    exit()
                LORD_Names.append(verse_reference)
            if '\\qt' in line:
                verse_reference=f"{Book_name} {last_chapter}:{line[3:].split()[0]}"
                if '*' not in line: 
                    echo(f"WARNING: Missing closing tag {verse_reference}",color=RED_DARK)
                    exit()
                OT_Quotes.append(verse_reference)

    with open(os.path.join(ROOT_PATH,"JESUS_Words.txt"),encoding='utf-8',mode='w') as f:
        f.write("\n".join(JESUS_Words))
    with open(os.path.join(ROOT_PATH,"LORD_Names.txt"),encoding='utf-8',mode='w') as f:
        f.write("\n".join(LORD_Names))
    with open(os.path.join(ROOT_PATH,"OT_Quotes.txt"),encoding='utf-8',mode='w') as f:
        f.write("\n".join(OT_Quotes))

def perform_automations():
    copy_original_to_paratext()
    # copy_original_to_text()
    make_single_text_file()
    form_log_files()

def monitor_files_for_changes():
    def get_last_modified_file():
        return max(ORIGINAL_FILES,key=os.path.getmtime)
    def get_modification_time(file:str):
        return os.path.getmtime(file)

    print("Automations script started")
    perform_automations()
    latest_file=get_last_modified_file()
    last_modification_time=get_modification_time(latest_file)
    while 1:
        latest_file=get_last_modified_file()
        current_modification_time=get_modification_time(latest_file)
        if last_modification_time!=current_modification_time:
            perform_automations()
            last_modification_time=current_modification_time
            # print(latest_file.split("\\")[-1][2:5],time.ctime(last_modification_time))
        time.sleep(1)

monitor_files_for_changes()