from dataclasses import dataclass
import os
import re

from code.Original_Automations import original_folder,code_folder

t='''
EXO 37:29 на кадило робом **мастиєльників**.
LEV 10:17 не **ззїли** ви жертви
LEV 16:18 **веред** Господом
LEV 22:14 коли хто ненароком **зʼість** сьвятого
NUM 32:9 добрались до долини **Эсколя** і розглянули землю;
DEU 11:25 вами **нагшле** Господь
1SA 14:42 повелїв **Саул. Жеребуйте** [крапка замість двокрапки]
1SA 18:11 Прибю **Давидаʼд** стїнї [немає пробіла перед 'д]
EST 2:4 було до **сподоби** се слово
JOB 13:8 вам **притворювятись** перед
JOB 15:10 **Е** й проміж нами
JOB 18:2 братись **за за** ум
JOB 21:3 як виговорюсь, **насьмівайтесь**.
JOB 27:20 прийде **ва** його неждано
JOB 33:23
JOB 41:22
PRO 16:33
ISA 6:2 **Кр угом** його стояли
ISA 49:20
ISA 63:19
JER 7:5
JER 14:10
JER 22:8
JER 23:40
JER 26:5
JER 30:20
JER 30:20
JER 31:13
JER 31:25
JER 32:2
JER 46:20
JER 48:3
JER 51:45
ZEC 1:15
ZEC 9:10
ZEC 10:6
ZEC 13:8 зіетанеться
ZEC 13:9 ймя мов
ZEC 14:5
ZEC 14:12
MAT 1:18
LUK 13:17 сталось від **Него?** [знак питання замість крапки]
ACT 6:14
ACT 14:26
ACT 17:24 землї Господь, не в рукотворних **хмарах** домує, [замість храмах]
ACT 21:16
ACT 22:2 говорив до них, ще більш **утихомирились.)** [немає відкриваючої дужки]
ROM 1:9
1CO 2:7
2CO 1:19
2CO 3:15
1TI 1:1
TIT 1:12
HEB 8:12
JAS 5:11
1PE 2:6
1PE 2:22
REV 11:8
'''.strip()
lines=t.split('\n')

Book_names=[]
for file_name in os.listdir(original_folder):
    Book=file_name[2:5]
    Book_names.append(Book)

@dataclass
class Entry:
    Book: str 
    chapter: int 
    verse: int 
    content: str 

entries:list[Entry]=[]
for line in lines:
    Book,other=line.split(maxsplit=1)
    chapter,others=other.split(':',maxsplit=1)
    try:
        verse,contents=others.split(' ',maxsplit=1)
    except:
        verse=others
        contents='-'
    entry=Entry(Book,int(chapter),int(verse),contents)
    entries.append(entry)

sorted_entries:list[Entry]=[]
for Book in Book_names:
    found_entries=[e for e in entries if e.Book==Book]
    sorted_found_entries=sorted(found_entries,key=lambda e:(e.chapter,e.verse),reverse=False)
    sorted_entries+=sorted_found_entries

table_lines=['| Book | Chapter | Verse | Content |','| - | - | - | - |']
for current_entry in sorted_entries:
    line=f'| {current_entry.Book} | {current_entry.chapter} | {current_entry.verse} | {current_entry.content} |'
    table_lines.append(line)

target_path=os.path.join(code_folder,'Table.md')
with open(target_path,encoding='utf-8',mode='w') as f:
    f.write('\n'.join(table_lines))