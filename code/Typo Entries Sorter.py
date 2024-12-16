from dataclasses import dataclass
import os
import re

from Automations import original_folder,code_folder

t='''
GEN 14:4 `чотирнайцятому` замість `тринайцятому`
GEN 9:29 `деватьсот`
GEN 11:3 нема коми перед а
GEN 43:19 нема символу пунктуації на кінці
EXO 12:42 `в роди і роди їх`
EXO 26:3 `калїми` і `келіїми`
EXO 34:22 `держатя меш`
EXO 37:29 `мастиєльників`
LEV 5:19 `дійсно` замість `існо`
DEU 17:8 `та`
DEU 16:22 verse missing
1SA 14:42 `.` замість `:`: `І повелїв Саул. Жеребуйте`
RUT 4:14 `жінки` замість `жінка`
PSA 58:11 `дійсно` замість `існо`
ISA 41:4 крапочка в кінці
ISA 42:2 `гнівний`
JER 18:13 `таке? (давна) дїва`
LUK 10:22 додати `turning to the disciples, HE said:`
LUK 13:17 крапочка в кінці: `І, як се промовив, засоромились усї противники Його, а всї люде радувались усїм славним, що сталось від Него?`
LUK 13:32 `скінчаюся` замість `звершуюся`: `I shall be perfected` (KJV)
LUK 23:34 додати `diving HIS Garments among them, they cast lots.`
JHN 8:58 `Я був` замість `Я Є`: `Before Abraham was, I AM` (KJV)
ACT 9:22 `у силу та в силу`
2TH 3:4 переписати `що що`
REV 15:6 `лнянку` замість `льняну`
REV 17:7 `Длячого` замість `Для чого`
ECC 4:5 може не має бути `приговорюючи:`
2SA 19:32 не знак питання на кінці мабуть
MAT 27:43 Слова Ісусові цитуються
MAT 27:63 Ісусові Слова цитуються
ISA 41:4 має бути не знак питання на кінці
LEV 5:23 `видусив`
LEV 8:15 `розгрішив`
LEV 8:36 `Мойсейя`
LEV 10:17 `ззїли`
NUM 32:9 літера `Э` замість `Є` у `Эсколя`: замінити на `Є`: у друкованій Біблії така літера і є
1KI 19:2 `те, саме` зайва кома
PSA 62:9 Відсутня крапочка на кінці
1CH 1:32 `(Сини Деданові: Рагуїл, Навдеїл, Ассурим, Летусим, Леюмим (Астусіїм, Асомин).` додано, а в ній додана `(Астусіїм, Асомин)`: прибрати другу дужку відкриваючу
ACT 17:24 `хмарах` замість `храмах`
JDG 7:1 `Еробаах` замість `Еробаал`
MRK 12:28 `пруступивши` замість `приступивши`
LEV 21:1 `не опоганюєть`
LEV 22:14 `зʼість`
NUM 27:20 `достойньства`
NUM 31:46 `людьких`
1SA 18:11 `Давидаʼд`
1SA 30:15 `тото`
1SA 30:15 `горду`
2SA 7:12 `спочнеш` замість `спочинеш`
2SA 8:1 `данини (Гет)`
1KI 11:41 `Инчі`
1KI 11:41 `Саломонових`
1KI 18:19 `Ізраїляа`
EST 2:4 `сподоби`
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
    verse,contents=others.split(' ',maxsplit=1)
    entry=Entry(Book,int(chapter),int(verse),contents)
    entries.append(entry)

sorted_entries:list[Entry]=[]
for Book in Book_names:
    found_entries=[e for e in entries if e.Book==Book]
    sorted_found_entries=sorted(found_entries,key=lambda e:(e.chapter,e.verse),reverse=False)
    sorted_entries+=sorted_found_entries

target_path=os.path.join(code_folder,'a.md')
with open(target_path,encoding='utf-8',mode='w') as f:
    for entry in sorted_entries:
        f.write(f'{entry.Book} {entry.chapter}:{entry.verse} {entry.content}\n')