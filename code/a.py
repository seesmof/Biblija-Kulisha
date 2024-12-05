import re

def get_verse_number(line:str) -> int:
    found_verses=re.findall(p,line)
    verse=found_verses[0]
    verse_number=verse[3:]
    return int(verse_number)

t=r'\v 1 In the beginning was the Word and the Word was with GOD and the Word was GOD.'
p=r'\\v\s\d+'
res=get_verse_number(t)
print(res)