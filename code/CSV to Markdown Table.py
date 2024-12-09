from dataclasses import dataclass
import os


@dataclass
class Entry:
    Book: str
    Chapter: int
    Verse: int
    Content: str


def convert_csv_lines_to_markdown_table(file_path: str, root_folder: str):
    with open(file_path, encoding="utf-8", mode="r") as f:
        lines = f.readlines()

    entries: list[Entry] = []
    for line in lines[1:]:
        split_line = line.strip().split(",", maxsplit=3)
        split_line[-1] = split_line[-1].replace('"', "")
        entry = Entry(*split_line)
        entries.append(entry)

    table = ["| Book | Chapter | Verse | Content |", "| - | - | - | - |"]
    for entry in entries:
        line = f"| {entry.Book} | {entry.Chapter} | {entry.Verse} | {entry.Content} |"
        table.append(line)

    output_path = os.path.join(root_folder, "Table.md")
    with open(output_path, encoding="utf-8", mode="w") as f:
        f.write("\n".join(table))


root_folder = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(root_folder, "..", "logs", "Apostrophes.csv")
convert_csv_lines_to_markdown_table(target_path, root_folder)
