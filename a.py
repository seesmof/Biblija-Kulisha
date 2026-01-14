import os

from code import util

source_folder_path: str = util.original_folder_path
output_lines = []
for file_name in os.listdir(source_folder_path):
    file_path = os.path.join(source_folder_path, file_name)
    lines = util.read_file_lines(file_path)
    Book_name = util.get_Book_name_from_full_file_name(file_name)
    chapter_number = 1

    for line in lines:
        if "\\c " in line:
            chapter_number = line[3:].split()[0]
        elif r"\v " in line:
            verse_text = line[3:].strip()
            stripped_formatting_tags = util.remove_formatting_usfm_tags(verse_text)
            removed_footnotes = util.remove_footnotes_and_crossreferences_with_contents(
                stripped_formatting_tags
            )
            removed_strongs_numbres = (
                util.remove_strongs_numbers(removed_footnotes)
                .strip()
                .replace("  ", " ")
            )
            line = f"{Book_name} {chapter_number}:{removed_strongs_numbres}"
            output_lines.append(line)
print(output_lines)
