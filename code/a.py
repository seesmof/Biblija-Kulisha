import re 

line=r'\v 15 Відказуючи йому Ісус, рече до него: \+wj Допусти тепер, бо так годить ся нам чинити всяку правду.\+wj* Тодї допустив Його.'
verse_number=re.findall(r'\\v\s\d+',line)[0][3:]
print(verse_number)
content=re.findall(r'\\\+?wj(.*?)\\\+?wj\*',line)
print("; ".join([c.strip() for c in content]))