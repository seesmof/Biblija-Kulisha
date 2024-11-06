import os
import re
import glob
import time
from shutil import copy2

ROOT_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
ORIGINAL_FILES_PATH=os.path.join(ROOT_PATH,"Original")
ORIGINAL_FILES=glob.glob(ORIGINAL_FILES_PATH+"\\*.USFM")
TEXT_FILES_PATH=os.path.join(ROOT_PATH,"Text")
LOG_FILES_PATH=os.path.join(ROOT_PATH,"logs")
PARATEXT_PROJECT_PATH=os.path.join("C:\\My Paratext 9 Projects\\BKS")
DEFAULT = '\033[0m'; BOLD = '\033[1m';ITALIC = '\033[3m';UNDERLINE = '\033[4m';UNDERLINE_THICK = '\033[21m';HIGHLIGHTED = '\033[7m';HIGHLIGHTED_BLACK = '\033[40m';HIGHLIGHTED_RED = '\033[41m';HIGHLIGHTED_GREEN = '\033[42m';HIGHLIGHTED_YELLOW = '\033[43m';HIGHLIGHTED_BLUE = '\033[44m';HIGHLIGHTED_PURPLE = '\033[45m';HIGHLIGHTED_CYAN = '\033[46m';HIGHLIGHTED_GREY = '\033[47m';HIGHLIGHTED_GREY_LIGHT = '\033[100m';HIGHLIGHTED_RED_LIGHT = '\033[101m';HIGHLIGHTED_GREEN_LIGHT = '\033[102m';HIGHLIGHTED_YELLOW_LIGHT = '\033[103m';HIGHLIGHTED_BLUE_LIGHT = '\033[104m';HIGHLIGHTED_PURPLE_LIGHT = '\033[105m';HIGHLIGHTED_CYAN_LIGHT = '\033[106m';HIGHLIGHTED_WHITE_LIGHT = '\033[107m';STRIKE_THROUGH = '\033[9m';MARGIN_1 = '\033[51m';MARGIN_2 = '\033[52m';BLACK = '\033[30m';RED_DARK = '\033[31m';GREEN_DARK = '\033[32m';YELLOW_DARK = '\033[33m';BLUE_DARK = '\033[34m';PURPLE_DARK = '\033[35m';CYAN_DARK = '\033[36m';GREY_DARK = '\033[37m';BLACK_LIGHT = '\033[90m';RED = '\033[91m';GREEN = '\033[92m';YELLOW = '\033[93m';BLUE = '\033[94m';PURPLE = '\033[95m';CYAN = '\033[96m';WHITE = '\033[97m';echo = lambda values, color=DEFAULT: print("%s%s%s" % (color, values, DEFAULT)) if color else print("%s%s" % (values, DEFAULT)) # source: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal#:~:text=%2C%20color%3DCYAN)-,1%20Line,-Simply%20copy%20paste
yes=lambda section,text:echo(f"{section.upper()}: {text}",color=CYAN_DARK)
fail=lambda section,text:echo(f"{section.upper()}: fail {text}",color=RED_DARK)
warn=lambda section,text:echo(f"{section.upper()}: {text}",color=BOLD)

def copy_original_to_paratext():
    section="PARA"
    try:
        for full_file_name in os.listdir(ORIGINAL_FILES_PATH):
            copy2(
                os.path.join(ORIGINAL_FILES_PATH,full_file_name),
                os.path.join(PARATEXT_PROJECT_PATH,full_file_name)
            )
    except: 
        fail(section,"copying files")
    yes(section,"copy files")

def write_file(
    section:str,
    file_name:str,
    lines:list,
    root:str=ROOT_PATH,
    tries:int=0
):
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
    return [
        l+'\n' 
        if i!=len(lines)-1 
        else l 
        for i,l in enumerate(lines)
    ]

def make_single_text_file():
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
    for full_file_name in os.listdir(ORIGINAL_FILES_PATH):
        try:
            target_file_path=os.path.join(ORIGINAL_FILES_PATH,full_file_name)
            with open(os.path.join(ORIGINAL_FILES_PATH,full_file_name),encoding='utf-8',mode='r') as f:
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

def form_log_files():
    JESUS_Words=[]
    LORD_Names=[]
    OT_Quotes=[]
    section="LOGS"
    for file_path in ORIGINAL_FILES:
        try:
            with open(file_path,encoding='utf-8',mode='r') as f:
                lines=f.readlines()
        except:
            fail(section,f"reading {file_path.split("\\")[-1]}")

        Book_name=lines[2].replace("\\h ","").strip()
        last_chapter=0
        for line in lines:
            if '\\c ' in line: 
                last_chapter=line[3:].strip()
            if '\\wj' in line or '\\+wj' in line:
                verse_reference=f"{Book_name} {last_chapter}:{line[3:].split()[0]}"
                if '*' not in line:
                    warn(verse_reference,"missing closing WJ tag")
                JESUS_Words.append(verse_reference)
            if '\\nd' in line or '\\+nd' in line:
                verse_reference=f"{Book_name} {last_chapter}:{line[3:].split()[0]}"
                if '*' not in line:
                    warn(verse_reference,"missing closing ND tag")
                LORD_Names.append(verse_reference)
            if '\\qt' in line or '\\+qt' in line:
                verse_reference=f"{Book_name} {last_chapter}:{line[3:].split()[0]}"
                if '*' not in line:
                    warn(verse_reference,"missing closing QT tag")
                OT_Quotes.append(verse_reference)

    write_file(section,"JESUS_Words.txt",combine_lines(JESUS_Words),LOG_FILES_PATH)
    write_file(section,"LORD_Names.txt",combine_lines(LORD_Names),LOG_FILES_PATH)
    write_file(section,"OT_Quotes.txt",combine_lines(OT_Quotes),LOG_FILES_PATH)
    yes(section,"form files")

def form_text_files_from_original(source_path:str=ORIGINAL_FILES_PATH):
    section="TEXT"
    for full_file_name in os.listdir(source_path):
        target_file_path=os.path.join(source_path,full_file_name)
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

            # Remove all WJ tags
            .replace("\\wj*","").replace("\\wj ","").replace("\\+wj*","").replace("\\+wj ","")
            # Remove all ND tags
            .replace("\\nd*","").replace("\\nd ","").replace("\\+nd*","").replace("\\+nd ","")
            # Remove all QT tags
            .replace("\\qt*","").replace("\\qt ","").replace("\\+qt*","").replace("\\+qt ","")
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

        write_file(section,full_file_name,lines,TEXT_FILES_PATH)
    yes(section,f"form files")

def perform_automations(last_time):
    print()
    # echo(time.ctime(last_time))

    copy_original_to_paratext()
    form_text_files_from_original()
    # make_single_text_file()
    # form_log_files()

def monitor_files_for_changes():
    def get_last_modified_file():
        return max(ORIGINAL_FILES,key=os.path.getmtime)
    def get_modification_time(file:str):
        return os.path.getmtime(file)

    echo("START")
    latest_file=get_last_modified_file()
    last_modification_time=get_modification_time(latest_file)
    perform_automations(last_modification_time)
    while 1:
        latest_file=get_last_modified_file()
        current_modification_time=get_modification_time(latest_file)
        if last_modification_time!=current_modification_time:
            perform_automations(last_modification_time)
            last_modification_time=current_modification_time
        time.sleep(1)

if __name__=="__main__":
    monitor_files_for_changes()