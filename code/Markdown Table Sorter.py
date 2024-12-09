# TODO add all the logs to changes and sort changes.csv
from dataclasses import dataclass
import os

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


@dataclass
class Change:
    Book: str
    Chapter: int
    Verse: int
    Mistake: str = ""
    Correction: str = ""
    Reason: str = "Wrong apostrophe"


def sort_markdown_table(file_path: str, root_folder: str):
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

    table_lines: list[str] = [
        "| Book | Chapter | Verse | Mistake | Correction | Reason |",
        "| - | - | - | - | - | - |",
    ]
    for Book in Ukrainian_Bible_Book_name_to_English_abbrevation.values():
        found_changes_for_this_Book = [
            change for change in changes if change.Book == Book
        ]
        print(found_changes_for_this_Book)
        found_changes = sorted(
            found_changes_for_this_Book,
            key=lambda change: (change.Chapter, change.Verse),
            reverse=False,
        )
        for change in found_changes:
            line = f"| {change.Book} | {change.Chapter} | {change.Verse} | {change.Mistake.replace('ʼ','\'') if change.Reason == 'Wrong apostrophe' else change.Mistake} | {change.Mistake if change.Reason=='Wrong apostrophe' else change.Correction} | {change.Reason} |"
            table_lines.append(line)

    print(table_lines)
    output_file = os.path.join(root_folder, "Table.md")
    with open(output_file, encoding="utf-8", mode="w") as f:
        f.write("\n".join(table_lines))


root_folder = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(root_folder, "..", "docs", "Checks", "Changes.md")
sort_markdown_table(target_path, root_folder)
