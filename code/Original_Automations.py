import shutil
import time
import os
import re
from tkinter import S

import util

original_docs_folder_path=os.path.join(util.docs_folder_path,'Original')
TBS_text_folder = os.path.join(original_docs_folder_path,'TBS')
original_logs_folder = os.path.join(original_docs_folder_path,'Logs')
changes_file = os.path.join(original_docs_folder_path,'Changes.md')
lined_output_file_path=os.path.join(original_docs_folder_path,'Output_Lined.txt')
formatted_original_output_file_path=os.path.join(original_docs_folder_path,'Output_Formatted.md')
revision_docs_folder_path=os.path.join(util.docs_folder_path,'Revision')
revision_logs_folder = os.path.join(revision_docs_folder_path,'Logs')
formatted_revision_output_file_path=os.path.join(revision_docs_folder_path,'Output_Formatted.md')

def copy_files_to_paratext_project(
    project_abbreviation: str = 'UBK',
    local_files_folder_path: str = util.original_folder_path,
    remove_comenting_rem_tags: bool = False,
):
    paratext_project_folder_path=os.path.join(util.paratext_projects_folder_path,project_abbreviation)
    for file_name in os.listdir(local_files_folder_path):
        paratext_file_path=os.path.join(paratext_project_folder_path,file_name)
        local_file_path=os.path.join(local_files_folder_path,file_name)
        shutil.copy2(local_file_path,paratext_file_path)

        if remove_comenting_rem_tags:
            lines=[l for l in util.read_file_lines(paratext_file_path) if not l.startswith(r'\rem ')]
            try:
                with open(paratext_file_path,encoding='utf-8',mode='w') as f:
                    f.write('\n'.join([l.strip() for l in lines]))
            except: pass

def remove_usfm_tags(line: str):
    # Remove WJ, ND, QT tags from the Bible verse line
    tags_to_remove = [
        "wj",
        "nd",
        "qt",
    ]
    for tag in tags_to_remove:
        line = line.replace(f"\\{tag} ", "").replace(f"\\{tag}*", "")
        # Replace those if they are indented as well
        # + sign marks an indented tag in USFM (a tag that is inside another tag)
        #   for example: when JESUS quotes from the Old Testament:
        #   Words of JESUS will be in \WJ and the quote will be in \QT
        line = line.replace(f"\\+{tag} ", "").replace(f"\\+{tag}*", "")

    # Footnotes begin with \f and ends with \f* always
    # Everything that is inbetween is selected also
    footnote_pattern = r"\\f(.*?)\\f\*"
    line = re.sub(footnote_pattern, "", line)
    return line

def form_logs(
    source_folder_path:str=util.revision_folder_path,
    output_folder_path:str=revision_logs_folder,
):
    def get_verse_number(line: str) -> int:
        verse_number_pattern = r"\\v\s\d+"
        # Look for verses inside the line
        found_verses = re.findall(verse_number_pattern, line)
        # Select first match because verse is usually at the beginning of the line
        verse = found_verses[0]
        # Strip the '\v ' text from it
        verse_number = verse[3:]
        # And return the number as integer
        return int(verse_number)

    header = "Book,Chapter,Verse,Content"
    WJ = [header]
    ND = [header]
    QT = [header]
    F = [header]
    Quotes = [header]
    Apostrophes = [header]
    Dashes = [header]

    for file_name in os.listdir(source_folder_path):
        file_path=os.path.join(source_folder_path,file_name)
        lines=util.read_file_lines(file_path)
        Book_name=util.get_Book_name_from_full_file_name(file_name)
        chapter_number = 0

        for line in lines:
            if "\\c " in line:
                chapter_number = line[3:].strip()

            if "\\wj" in line or "\\+wj" in line:
                verse_number = get_verse_number(line)
                contents = re.findall(r"\\\+?wj\s(.*?)\\\+?wj\*", line)
                for c in contents:
                    res = f'{Book_name},{chapter_number},{verse_number},"{remove_usfm_tags(c)}"'
                    WJ.append(res)
            if "\\nd" in line or "\\+nd" in line:
                verse_number = get_verse_number(line)
                contents = re.findall(r"\\\+?nd\s(.*?)\\\+?nd\*", line)
                for c in contents:
                    res = f'{Book_name},{chapter_number},{verse_number},"{remove_usfm_tags(c)}"'
                    ND.append(res)
            if "\\qt" in line or "\\+qt" in line:
                verse_number = get_verse_number(line)
                contents = re.findall(r"\\\+?qt\s(.*?)\\\+?qt\*", line)
                for c in contents:
                    res = f'{Book_name},{chapter_number},{verse_number},"{remove_usfm_tags(c)}"'
                    QT.append(res)
            if "\\f" in line or "\\+f" in line:
                contents = re.findall(r"\\\+?ft\s(.*?)\\\+?f\*", line)
                if "\\mt" in line:
                    for entry in contents:
                        F.append(f'{Book_name},0,0,"{remove_usfm_tags(entry)}"')
                else:
                    verse_number = get_verse_number(line)
                    for c in contents:
                        res = f'{Book_name},{chapter_number},{verse_number},"{remove_usfm_tags(c)}"'
                        F.append(res)
            line = remove_usfm_tags(line)
            if "„" in line or "‟" in line:
                verse_number = get_verse_number(line)
                contents = [w for w in line.split() if "„" in w or "‟" in w]
                for c in contents:
                    res = f'{Book_name},{chapter_number},{verse_number},"{remove_usfm_tags(c)}"'
                    Quotes.append(res)
            if "ʼ" in line:
                verse_number = get_verse_number(line)
                contents = [w for w in line.split() if "ʼ" in w]
                for c in contents:
                    res = f'{Book_name},{chapter_number},{verse_number},"{remove_usfm_tags(c)}"'
                    Apostrophes.append(res)
            if "—" in line:
                verse_number = get_verse_number(line)
                pattern = r"\w+\s*—|\W\s*—"
                contents = re.findall(pattern, line)
                for c in contents:
                    res = f'{Book_name},{chapter_number},{verse_number},"{remove_usfm_tags(c)}"'
                    Dashes.append(res)

    try:
        with open(os.path.join(output_folder_path, "WJ.csv"), encoding="utf-8", mode='w') as f:
            f.write("\n".join(WJ))
    except: pass

    try:
        with open(os.path.join(output_folder_path, "ND.csv"), encoding="utf-8", mode='w') as f:
            f.write("\n".join(ND))
    except: pass

    try:
        with open(os.path.join(output_folder_path, "QT.csv"), encoding="utf-8", mode='w') as f:
            f.write("\n".join(QT))
    except: pass

    try:
        with open(os.path.join(output_folder_path, "F.csv"), encoding="utf-8", mode='w') as f:
            f.write("\n".join(F))
    except: pass

    try:
        with open(os.path.join(output_folder_path, "Quotes.csv"), encoding="utf-8", mode='w') as f:
            f.write("\n".join(Quotes))
    except: pass

    try:
        with open(os.path.join(output_folder_path, "Apostrophes.csv"),encoding="utf-8",mode='w',) as f:
            f.write("\n".join(Apostrophes))
    except: pass

    try:
        with open(os.path.join(output_folder_path, "Dashes.csv"), encoding="utf-8", mode='w') as f:
            f.write("\n".join(Dashes))
    except: pass

def make_tbs_text_files(
    folder_path:str=util.original_folder_path,
):
    for file_name in os.listdir(folder_path):
        Book_name=util.get_Book_name_from_full_file_name(file_name)
        file_path=os.path.join(folder_path,file_name)
        lines=util.read_file_lines(file_path)

        needed_tags=['toc','v','s','c']
        lines=[line for line in lines if any(tag in line for tag in needed_tags)]
        for i,line in enumerate(lines):
            lines[i]=lines[i].replace('[','*').replace(']','*')
            lines[i]=re.sub(r'\\f\s\+\s\\ft\s','[',lines[i]).replace(r'\f*',']').replace(r'\v ','#').replace(r'\c ','##').replace(r'\toc2','###!').replace(r'\toc1','###!!')
            lines[i]=re.sub(r'\\s\d+','##!',lines[i])
            lines[i]=util.remove_formatting_usfm_tags(lines[i])
        lines=[f'###{Book_name}']+lines
    
        output_file_path=os.path.join(original_docs_folder_path,'TBS',file_name[2:].replace('USFM','TXT'))
        try:
            with open(output_file_path,encoding='utf-8',mode='w') as f:
                f.write('\n'.join([l.strip() for l in lines]))
        except: pass


def sort_markdown_table(
    file_path: str
):
    lines=util.read_file_lines(file_path)
    changes: list[util.ChangeEntry] = []
    for line in lines[2:]:
        split_line = line.strip()[2:-2].split(" | ")
        change = util.ChangeEntry(*split_line)
        change.Chapter = int(change.Chapter)
        change.Verse = int(change.Verse)
        changes.append(change)

    sorted_table_lines: list[str] = [
        "| Book | Chapter | Verse | Mistake | Correction | Reason |",
        "| - | - | - | - | - | - |",
    ]

    # get all Book names
    Book_names: list[str] = []
    for file in os.listdir(util.original_folder_path):
        Book_names.append(file[2:5])

    for Book in Book_names:
        found_changes_for_this_Book = [
            change for change in changes if change.Book == Book
        ]
        found_changes = sorted(
            found_changes_for_this_Book,
            key=lambda change: (change.Chapter, change.Verse),
            reverse=False,
        )
        for change in found_changes:
            line = f"| {change.Book} | {change.Chapter} | {change.Verse} | {change.Mistake} | {change.Correction} | {change.Reason} |"
            sorted_table_lines.append(line)

    try:
        with open(file_path, encoding="utf-8", mode='w') as f:
            f.write("\n".join(sorted_table_lines))
    except: pass


def form_text_lined(
    source_folder_path:str=util.original_folder_path,
    vault_output_file_path:str=r"E:\Notatnyk\Біблія Куліша.txt",
    local_output_file_path:str=None,
):
    output_lines = []
    for file_name in os.listdir(source_folder_path):
        file_path=os.path.join(source_folder_path,file_name)
        lines=util.read_file_lines(file_path)
        Book_name=util.get_Book_name_from_full_file_name(file_name)
        chapter_number = 1

        for line in lines:
            if "\\c " in line:
                chapter_number = line[3:].split()[0]
            elif r'\v ' in line:
                verse_text = line[3:].strip()
                stripped_formatting_tags=util.remove_formatting_usfm_tags(verse_text)
                removed_footnotes=util.remove_footnotes_with_contents(stripped_formatting_tags)
                removed_strongs_numbres=util.remove_strongs_numbers(removed_footnotes).strip().replace('  ',' ')
                line = f"{Book_name} {chapter_number}:{removed_strongs_numbres}"
                output_lines.append(line)
    try:
        if local_output_file_path:
            with open(local_output_file_path,encoding='utf-8',mode='w') as f:
                f.write('\n'.join(output_lines))
        if 'Notatnyk' not in vault_output_file_path:
            vault_output_file_path=os.path.join(r'E:\Notatnyk',vault_output_file_path)
        with open(vault_output_file_path,encoding='utf-8',mode='w') as f:
            f.write('\n'.join(output_lines))
    except: pass


def form_markdown_output(
    source_folder_path:str = util.original_folder_path,
    local_output_file_path:str=formatted_original_output_file_path,
    vault_output_file_path:str=r'E:\Notatnyk\Біблія Куліша.md',
):
    output_lines=[]
    for file_name in os.listdir(source_folder_path):
        file_path=os.path.join(source_folder_path,file_name)
        lines=util.read_file_lines(file_path)
        Book_name=util.get_Book_name_from_full_file_name(file_name)
        output_lines.append(f'# {Book_name}')
        
        for line in lines:
            if r'\c ' in line:
                chapter_number=line[3:].strip()
                res=f'### {Book_name} {chapter_number}'
                output_lines.append(res)
            elif r'\p' in line:
                output_lines.append('')
            elif r'\v ' in line:
                WJ_COLOR='#7e1717'
                line=line[3:].strip()
                verse_number,contents=line.split(maxsplit=1)
                contents=util.remove_strongs_numbers(contents)
                contents=re.sub(r'\\(\+?)qt\s',f'<span style="font-variant: small-caps">',contents)
                contents=re.sub(r'\\(\+?)nd\s',f'<span style="font-variant: small-caps; font-weight:bold">',contents)
                contents=re.sub(r'\\(\+?)wj\s',f'<span style="color: {WJ_COLOR}">',contents)
                contents=re.sub(r'\\(\+?)add\s','<em>',contents)
                contents=contents.replace('\\add*','</em>').replace('\\+add*','</em>')
                contents=util.remove_footnotes_with_contents(contents)
                # all other closing tags
                contents=re.sub(r'\\(\+?)\w+\*','</span>',contents)
                res=f'<sup>{verse_number}</sup> {contents}'
                output_lines.append(res)

    try:
        if local_output_file_path:
            with open(local_output_file_path,encoding='utf-8',mode='w') as f:
                f.write('\n'.join(output_lines))
        if 'Notatnyk' not in vault_output_file_path:
            vault_output_file_path=os.path.join(r'E:\Notatnyk',vault_output_file_path)
        with open(vault_output_file_path,encoding='utf-8',mode='w') as f:
            f.write('\n'.join(output_lines))
    except: pass

def perform_automations():
    print()
    copy_files_to_paratext_project()
    print('Paratext Original')
    copy_files_to_paratext_project('UFB',util.revision_folder_path,True)
    print('Paratext Revision')
    make_tbs_text_files()
    print('TBS Original')
    form_markdown_output()
    print('Formatted Original')
    form_markdown_output(util.revision_folder_path,formatted_revision_output_file_path,r'E:\Notatnyk\Біблія свободи.md')
    print('Formatted Revision')
    form_markdown_output(source_folder_path=r"E:\Pisochnycja-Projektiv\Bible Kulish\KJV_Strongs",local_output_file_path=None,vault_output_file_path=r'E:\Notatnyk\Біблія Короля Якова.md')
    print('Formatted KJV')
    form_text_lined(vault_output_file_path=r'Біблія Куліша.txt')
    print('Lined Original')
    form_text_lined(source_folder_path=r"E:\Pisochnycja-Projektiv\Bible Kulish\KJV_Strongs",vault_output_file_path=r'Біблія Короля Якова.txt')
    print('Lined KJV')
    form_logs(util.original_folder_path,original_logs_folder)
    print('Logs Original')
    form_logs()
    print('Logs Revision')
    # sort_markdown_table(changes_file)
    # print('Sort the changes table for Original')

def watch_folder_for_changes():
    file_paths=[os.path.join(util.original_folder_path,file_name) for file_name in os.listdir(util.original_folder_path)]+[os.path.join(util.revision_folder_path,file_name) for file_name in os.listdir(util.revision_folder_path)]
    last_modified_file = max(file_paths, key=os.path.getmtime)
    last_modification_time = os.path.getmtime(last_modified_file)
    perform_automations()
    while 1:
        last_modified_file = max(file_paths, key=os.path.getmtime)
        current_modification_time = os.path.getmtime(last_modified_file)
        if last_modification_time != current_modification_time:
            perform_automations()
            last_modification_time = current_modification_time
        time.sleep(1)

if __name__ == "__main__":
    watch_folder_for_changes()