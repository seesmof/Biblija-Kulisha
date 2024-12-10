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
