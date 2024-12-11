from dataclasses import dataclass
from shutil import copy2
import glob
import time
import os
import re

Ukrainian_Bible_Book_name_to_English_abbrevation = {
    "1 Мойсея": "GEN",
    "2 Мойсея": "EXO",
    "3 Мойсея": "LEV",
    "4 Мойсея": "NUM",
    "5 Мойсея": "DEU",
    "Иозея": "JOS",
    "Суддїв": "JDG",
    "Рути": "RUT",
    "1 Самуїлова": "1SA",
    "2 Самуїлова": "2SA",
    "1 Царів": "1KI",
    "2 Царів": "2KI",
    "1 Паралипоменон": "1CH",
    "2 Паралипоменон": "2CH",
    "Ездри": "EZR",
    "Неємії": "NEH",
    "Естери": "EST",
    "Йова": "JOB",
    "Псалтирь": "PSA",
    "Приповісток": "PRO",
    "Екклезіаста": "ECC",
    "Пісень": "SNG",
    "Ісаїї": "ISA",
    "Еремії": "JER",
    "Плач": "LAM",
    "Езекиїла": "EZK",
    "Даниїла": "DAN",
    "Осії": "HOS",
    "Йоіла": "JOL",
    "Амоса": "AMO",
    "Авдія": "OBA",
    "Йони": "JON",
    "Михея": "MIC",
    "Наума": "NAM",
    "Аввакума": "HAB",
    "Софонії": "ZEP",
    "Аггея": "HAG",
    "Захарії": "ZEC",
    "Малахія": "MAL",
    "Маттея": "MAT",
    "Марка": "MRK",
    "Луки": "LUK",
    "Йоана": "JHN",
    "Дїяння": "ACT",
    "Римлян": "ROM",
    "1 Коринтян": "1CO",
    "2 Коринтян": "2CO",
    "Галат": "GAL",
    "Єфесян": "EPH",
    "Филипян": "PHP",
    "Колосян": "COL",
    "1 Солунян": "1TH",
    "2 Солунян": "2TH",
    "1 Тимотея": "1TI",
    "2 Тимотея": "2TI",
    "Тита": "TIT",
    "Филимона": "PHM",
    "Жидів": "HEB",
    "Якова": "JAS",
    "1 Петра": "1PE",
    "2 Петра": "2PE",
    "1 Йоана": "1JN",
    "2 Йоана": "2JN",
    "3 Йоана": "3JN",
    "Юди": "JUD",
    "Одкриттє": "REV",
}

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
code_folder_path = os.path.dirname(os.path.abspath(__file__))
original_folder_path = os.path.join(root, "Original")
original_file_paths = glob.glob(original_folder_path + "\\*.USFM")
output_folder_path = os.path.join(root, "Output")
text_TBS_folder_path = os.path.join(output_folder_path, "TXT TBS")
text_solid_folder_path = os.path.join(output_folder_path, "TXT SLD")
text_lined_folder_path = os.path.join(output_folder_path, "TXT LND")
logs_folder_path = os.path.join(root, "logs")
paratext_folder_path = os.path.join("C:\\My Paratext 9 Projects\\BKS")
changes_table_file_path = os.path.join(root, "docs", "Checks", "Changes.md")


@dataclass
class Change:
    Book: str
    Chapter: int
    Verse: int
    Mistake: str
    Correction: str
    Reason: str


def copy_to_paratext():
    try:
        for file_path in original_file_paths:
            copy2(
                file_path, os.path.join(paratext_folder_path, file_path.split("\\")[-1])
            )
    except:
        pass


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
        print(found_verses)
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

    for file_path in original_file_paths:
        with open(file_path, encoding="utf-8", mode="r") as f:
            lines = f.readlines()

        Book_name = lines[2].replace("\\h ", "").strip()
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
        with open(
            os.path.join(logs_folder_path, "WJ.csv"), encoding="utf-8", mode="w"
        ) as f:
            f.write("\n".join(WJ))
    except:
        pass

    try:
        with open(
            os.path.join(logs_folder_path, "ND.csv"), encoding="utf-8", mode="w"
        ) as f:
            f.write("\n".join(ND))
    except:
        pass

    try:
        with open(
            os.path.join(logs_folder_path, "QT.csv"), encoding="utf-8", mode="w"
        ) as f:
            f.write("\n".join(QT))
    except:
        pass

    try:
        with open(
            os.path.join(logs_folder_path, "F.csv"), encoding="utf-8", mode="w"
        ) as f:
            f.write("\n".join(F))
    except:
        pass

    try:
        with open(
            os.path.join(logs_folder_path, "Quotes.csv"), encoding="utf-8", mode="w"
        ) as f:
            f.write("\n".join(Quotes))
    except:
        pass

    try:
        with open(
            os.path.join(logs_folder_path, "Apostrophes.csv"),
            encoding="utf-8",
            mode="w",
        ) as f:
            f.write("\n".join(Apostrophes))
    except:
        pass

    try:
        with open(
            os.path.join(logs_folder_path, "Dashes.csv"), encoding="utf-8", mode="w"
        ) as f:
            f.write("\n".join(Dashes))
    except:
        pass


def form_text_tbs():
    for file_path in original_file_paths:
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
            # Replace `[ ]` with `* *`
            .replace("[", "*").replace("]", "*")
            # Remove USFM formatting tags
            .replace("\\wj ", "")
            .replace("\\wj*", "")
            .replace("\\+wj ", "")
            .replace("\\+wj*", "")
            .replace("\\nd ", "")
            .replace("\\nd*", "")
            .replace("\\+nd ", "")
            .replace("\\+nd*", "")
            .replace("\\qt ", "")
            .replace("\\qt*", "")
            .replace("\\+qt ", "")
            .replace("\\+qt*", "")
            for line in lines
        ]
        lines = [
            # Put chapter number lines on a separate line
            (
                line[:-1] + "\n"
                if re.search(r"##\d+\s", line)
                # If its not a chapter number, then write it as it is
                else line
            )
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
            with open(
                os.path.join(text_TBS_folder_path, full_name),
                encoding="utf-8",
                mode="w",
            ) as f:
                f.writelines(lines)
        except:
            pass


def form_text_solid():
    all_lines = []
    for file_path in original_file_paths:
        with open(file_path, encoding="utf-8", mode="r") as f:
            lines = f.readlines()
        lines = [
            remove_usfm_tags(
                # Match verse tags and numbers and remove them
                re.sub(r"\\v\s\d+\s", "", line)
            )
            for line in lines
            if "\\p" not in line
            and "\\c" not in line
            and "\\id" not in line
            and "\\h" not in line
            and "\\toc1" not in line
            and "\\toc2" not in line
            and "\\toc3" not in line
            and "\\mt" not in line
        ]
        all_lines += lines
    # Join everything into one solid wall of text, ALLELUJAH JESUS THANK YOU LORD GOD ALMIGHTY!
    res = " ".join(
        # Replace all new line tags
        [line.replace("\n", "") for line in all_lines]
    )
    try:
        with open(
            os.path.join(text_solid_folder_path, "Solid.txt"),
            encoding="utf-8",
            mode="w",
        ) as f:
            f.write(res)
    except:
        pass


def form_text_lined():
    avoid_these = [
        "p",
        "id",
        "h",
        "mt",
        "toc1",
        "toc2",
        "toc3",
    ]
    all_lines = []
    for file_path in original_file_paths:
        with open(file_path, encoding="utf-8", mode="r") as f:
            lines = f.readlines()
        Book_name = lines[2][3:].strip()
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
        with open(
            os.path.join(text_lined_folder_path, "Lined.txt"),
            encoding="utf-8",
            mode="w",
        ) as f:
            f.write("\n".join(all_lines))
    except:
        pass


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

    for i, change in enumerate(changes):
        if change.Book in Ukrainian_Bible_Book_name_to_English_abbrevation:
            changes[i].Book = Ukrainian_Bible_Book_name_to_English_abbrevation[
                change.Book
            ]

    sorted_table_lines: list[str] = [
        "| Book | Chapter | Verse | Mistake | Correction | Reason |",
        "| - | - | - | - | - | - |",
    ]
    for Book in Ukrainian_Bible_Book_name_to_English_abbrevation.values():
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
    copy_to_paratext()
    print("Copied Bible files to Paratext")
    form_text_tbs()
    print("Formed TBS Bible text files")
    form_text_solid()
    print("Formed solid Bible text file")
    form_text_lined()
    print("Formed lined Bible text file")
    form_logs()
    print("Formed log files")
    sort_markdown_table(changes_table_file_path)
    print("Sorted changes table")


def monitor_files_for_changes():
    latest_file = max(original_file_paths, key=os.path.getmtime)
    last_modification_time = os.path.getmtime(latest_file)
    perform_automations()
    while 1:
        latest_file = max(original_file_paths, key=os.path.getmtime)
        current_modification_time = os.path.getmtime(latest_file)
        if last_modification_time != current_modification_time:
            perform_automations()
            last_modification_time = current_modification_time
        time.sleep(1)


if __name__ == "__main__":
    monitor_files_for_changes()
