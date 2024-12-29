import re

def remove_footnotes_with_text(verse: str):
    footnote_pattern=r'\\(\+*)f(.*?)\\(\+*)f\*'
    return re.sub(footnote_pattern,'',verse)

def remove_formatting_usfm_tags(verse: str):
    tags_pattern=r'\\(\+*)(wj|qt|nd)(\s|\*)'
    return re.sub(tags_pattern,'',verse)

def remove_verse_tags_and_numbers(verse: str):
    verse_tag_and_number_pattern=r'\\v\s\d+\s'
    return re.sub(verse_tag_and_number_pattern,'',verse)
