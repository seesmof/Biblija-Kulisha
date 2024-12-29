from dataclasses import dataclass
import os

from code.Original_Automations import root,code_folder,original_folder

target_file=os.path.join(root,'docs','Typos.md')
with open(target_file, encoding="utf-8", mode="r") as f:
    lines = f.readlines()

@dataclass
class Typo:
    Book: str 
    Chapter: int 
    Verse: int 
    Mistake: str 

typos: list[Typo] = []
suitable_lines=[line for line in lines if '|' in line]
for line in suitable_lines[2:]:
    split_line = line.strip()[2:-2].split(" | ")
    typo = Typo(*split_line)
    typo.Chapter = int(typo.Chapter)
    typo.Verse = int(typo.Verse)
    typos.append(typo)

sorted_table_lines: list[str] = [
    "| Book | Chapter | Verse | Mistake |",
    "| - | - | - | - |",
]

Book_names: list[str] = []
for file in os.listdir(original_folder):
    Book_names.append(file[2:5])

for Book in Book_names:
    found_typos_for_this_Book = [
        typo for typo in typos if typo.Book == Book
    ]
    found_typos = sorted(
        found_typos_for_this_Book,
        key=lambda typo: (typo.Chapter, typo.Verse),
        reverse=False,
    )
    for typo in found_typos:
        line = f"| {typo.Book} | {typo.Chapter} | {typo.Verse} | {typo.Mistake} |"
        sorted_table_lines.append(line)

output_file=os.path.join(code_folder,'Table.md')
with open(output_file, encoding="utf-8", mode="w") as f:
    f.write("\n".join(sorted_table_lines))