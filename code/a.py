import os
import re
from Automations import Ukrainian_Bible_Book_name_to_English_abbrevation
from dataclasses import dataclass


@dataclass
class Change:
    Book: str
    Chapter: int
    Verse: int
    Mistake: str
    Correction: str = ""
    Reason: str = "Extra symbol"


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


typos_load = """
1KI 18 19
1SA 18 11
REV 11 8
JER 51 45 
1KI 11 41 
JER 48 3 
2CO 3 15 
1KI 8 17 
LEV 22 14 
1KI 7 6 
LEV 21 1 
2CO 1 19 
LEV 16 18 
1KI 1 33 
JOB 41 22 
LEV 13 55 
ISA 49 20 
LEV 10 17 
ISA 63 19 
Acts 15 10
Acts 15 11
Жидів 8 12
1 Тимотея 1 1
Еремії 7 5
Йова 13 8
Йова 13 16
1 Самуїлова 27 3
2 Мойсея 26 3
Йова 14 14
2 Мойсея 27 18
Йова 15:10
Дїяння 21:16
Приповісток 16:33
Римлян 1:9
1 Самуїлова 30:15
2 Мойсея 30:34
Йова 18:2
Еремії 14:10
Йова 21:3
2 Мойсея 33 3 
2 Мойсея 34 22
Тита 1 12
2 Мойсея 37 29
2 Самуїлова 7 12
Псалом 88 18
2 Самуїлова 8 1
Еремії 22 8
Еремії 23 40
Маттея 1 18
Дїяння 6 14
Якова 5 11
Ісаїї 6 2 
Еремії 26 5
Захарії 14 12
2 Самуїлова 13 3
Захарії 9 10
1 Петра 2 6
1 Петра 2 22
Еремії 32 2
Естери 2 4 
3 Мойсея 5 3
3 Мойсея 5 23
Йова 33 23
Захарії 14 5
1 Коринтян 2 7
Еремії 30 20
Захарії 1 15
Захарії 10 6
Еремії 31 13
Еремії 31 25
5 Мойсея 11 25
Еремії 46 20
Еремії 30 20
3 Мойсея 8 15
3 Мойсея 8 36 
Захарії 13 8 
Захарії 13 9 
2 Паралипоменон 3 14
Дїяння 14 26
""".strip()


@dataclass
class BibleReference:
    Book: str
    Chapter: int
    Verse: int


references: list[BibleReference] = []
for typo in typos_load.split("\n"):
    typo = typo.strip()
    Book = re.findall(r"\d*\s*\w+\s", typo)
    rest = typo.replace(Book[0], "")
    chapter, verse = re.split(r"[\s\:]", rest)
    ref = BibleReference(Book[0].strip(), chapter, verse)
    references.append(ref)
for i, ref in enumerate(references):
    if ref.Book in Ukrainian_Bible_Book_name_to_English_abbrevation:
        references[i].Book = Ukrainian_Bible_Book_name_to_English_abbrevation[ref.Book]
table = list()
for Book in Ukrainian_Bible_Book_name_to_English_abbrevation.values():
    found_references_for_this_Book = [
        reference for reference in references if reference.Book == Book
    ]
    sorted_references = sorted(
        found_references_for_this_Book,
        key=lambda ref: (int(ref.Chapter), int(ref.Verse)),
        reverse=False,
    )
    for ref in sorted_references:
        table.append(f"{ref.Book} {ref.Chapter}:{ref.Verse}")
root_folder = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(root_folder, "Table.md")
with open(target_path, encoding="utf-8", mode="w") as f:
    f.write("\n".join(table))
