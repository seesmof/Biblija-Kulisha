from dataclasses import dataclass
from shutil import copy2
import glob
import time
import os
import re

import util

original_files = glob.glob(util.original_folder_path + "\\*.USFM")
original_docs_folder_path=os.path.join(util.docs_folder_path,'Original')
TBS_text_folder = os.path.join(original_docs_folder_path,'TBS')
logs_folder = os.path.join(original_docs_folder_path,'Logs')
changes_file = os.path.join(original_docs_folder_path,'Changes.md')
lined_output_file_path=os.path.join(original_docs_folder_path,'Output_Lined.txt')

@dataclass
class Change:
    Book: str
    Chapter: int
    Verse: int
    Mistake: str
    Correction: str
    Reason: str

def copy_files_to_paratext_project(
    project_abbreviation: str = 'UBK', 
    local_files_folder_path: str = util.original_folder_path,
):
    paratext_project_folder_path=os.path.join(util.paratext_projects_folder_path,project_abbreviation)
    for file_name in os.listdir(local_files_folder_path):
        paratext_file_path=os.path.join(paratext_project_folder_path,file_name)
        local_file_path=os.path.join(local_files_folder_path,file_name)
        copy2(local_file_path,paratext_file_path)

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

def form_logs():
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

    for file_name in os.listdir(util.revision_folder_path):
        file_path=os.path.join(util.revision_folder_path,file_name)
        with open(file_path, encoding="utf-8", mode="r") as f:
            lines = f.readlines()

        Book_name = file_name[2:].replace('.USFM','')
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
        with open(os.path.join(logs_folder, "WJ.csv"), encoding="utf-8", mode="w") as f:
            f.write("\n".join(WJ))
    except: pass

    try:
        with open(os.path.join(logs_folder, "ND.csv"), encoding="utf-8", mode="w") as f:
            f.write("\n".join(ND))
    except: pass

    try:
        with open(os.path.join(logs_folder, "QT.csv"), encoding="utf-8", mode="w") as f:
            f.write("\n".join(QT))
    except: pass

    try:
        with open(os.path.join(logs_folder, "F.csv"), encoding="utf-8", mode="w") as f:
            f.write("\n".join(F))
    except: pass

    try:
        with open(os.path.join(logs_folder, "Quotes.csv"), encoding="utf-8", mode="w") as f:
            f.write("\n".join(Quotes))
    except: pass

    try:
        with open(os.path.join(logs_folder, "Apostrophes.csv"),encoding="utf-8",mode="w",) as f:
            f.write("\n".join(Apostrophes))
    except: pass

    try:
        with open(os.path.join(logs_folder, "Dashes.csv"), encoding="utf-8", mode="w") as f:
            f.write("\n".join(Dashes))
    except: pass


def form_text_tbs():
    for file_path in original_files:
        with open(file_path, encoding="utf-8", mode="r") as f:
            lines = f.readlines()

        lines = [
            line
            for line in lines
            # Remove `\ide`
            if "\\ide" not in line
            # Remove `\h`
            and "\\h" not in line
            # Remove `\toc3`
            and "\\toc3" not in line
            # Remove `\mt`
            and "\\mt" not in line
            # Remove `\p`
            and "\\p" not in line
        ]
        lines = [
            line
            # Remove ` - Biblija Kulisha Standartna`
            .replace(" - Biblija Kulisha Standartna", "")
            # Change `\id ` to `###`
            .replace("\\id ", "###")
            # Change `\toc1 ` to `###!!`
            .replace("\\toc1", "###!!")
            # Change `\toc2 ` to `###!`
            .replace("\\toc2", "###!")
            # Change `\c ` to `##`
            .replace("\\c ", "##")
            # Change `\v ` to `#`
            .replace("\\v ", "#")
            # Change `\s1 ` to `##!`
            .replace("\\s1", "##!")
            # Replace `[ ]` with `* *`
            .replace("[", "*").replace("]", "*")
            # Remove USFM formatting tags
            .replace("\\wj ", "").replace("\\wj*", "").replace("\\+wj ", "").replace("\\+wj*", "")
            .replace("\\nd ", "").replace("\\nd*", "").replace("\\+nd ", "").replace("\\+nd*", "")
            .replace("\\qt ", "").replace("\\qt*", "").replace("\\+qt ", "").replace("\\+qt*", "")
            for line in lines
        ]
        lines = [
            re.sub(r"\\f\s\+\s\\ft\s", "[", line).replace("\\f*", "]") for line in lines
        ]

        file_name, file_extension = file_path.split("\\")[-1].split(".")
        # Remove number and BKS from filename
        # So `41MATBKS` will be `MAT`
        file_name = file_name[2:].replace("BKS", "")
        # Change file extension and form full name
        file_extension = "TXT"
        full_name = f"{file_name}.{file_extension}"

        try:
            with open(os.path.join(TBS_text_folder, full_name),encoding="utf-8",mode="w") as f:
                f.writelines(lines)
        except: pass

def form_text_lined():
    avoid_these = [
        "p",
        "id",
        "h",
        "mt",
        "toc",
        'rem',
    ]
    all_lines = []
    for file_name in os.listdir(util.original_folder_path):
        file_path=os.path.join(util.original_folder_path,file_name)
        with open(file_path, encoding="utf-8", mode="r") as f:
            lines = f.readlines()
        Book_name = file_name[2:5]
        chapter_number = 1
        for line in lines:
            if any(tag in line for tag in avoid_these):
                continue
            if "\\c " in line:
                chapter_number = line[3:].split()[0]
                continue
            # Remove the `\v ` tag from line
            verse_text = line[3:].strip()
            line = f"{Book_name} {chapter_number}:{remove_usfm_tags(verse_text)}"
            all_lines.append(line)
    try:
        with open(lined_output_file_path,encoding="utf-8",mode="w") as f:
            f.write("\n".join(all_lines))
    except: pass

def sort_markdown_table(file_path: str):
    with open(file_path, encoding="utf-8", mode="r") as f:
        lines = f.readlines()

    changes: list[Change] = []
    for line in lines[2:]:
        split_line = line.strip()[2:-2].split(" | ")
        change = Change(*split_line)
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

    with open(file_path, encoding="utf-8", mode="w") as f:
        f.write("\n".join(sorted_table_lines))

def perform_automations():
    print()
    copy_files_to_paratext_project()
    print("Paratext")
    form_text_tbs()
    print("TBS")
    form_text_lined()
    print("TXT")
    form_logs()
    print("Logs")
    sort_markdown_table(changes_file)
    print("Changes")

def monitor_files_for_changes():
    latest_file = max(original_files, key=os.path.getmtime)
    last_modification_time = os.path.getmtime(latest_file)
    perform_automations()
    while 1:
        latest_file = max(original_files, key=os.path.getmtime)
        current_modification_time = os.path.getmtime(latest_file)
        if last_modification_time != current_modification_time:
            perform_automations()
            last_modification_time = current_modification_time
        time.sleep(1)

if __name__ == "__main__":
    monitor_files_for_changes()