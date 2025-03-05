from collections import defaultdict
import json
file_path=r"E:\Biblija-Kulisha\docs\Original\UBK.json"

with open(file_path,encoding='utf-8',mode='r') as f:
    loaded_dictionary: dict = json.load(f)

numbered_dictionary: dict = defaultdict(dict)
for Book_number,Book_contents in loaded_dictionary.items():
    Book_number=int(Book_number)
    numbered_dictionary[Book_number]=dict()
    for chapter_number,chapter_contents in loaded_dictionary[Book_number].items():
        chapter_number=int(chapter_number)
        numbered_dictionary[Book_number]