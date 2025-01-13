from dataclasses import dataclass
import os

from util import *

t='''
GEN 9:29 `деватьсот`
GEN 11:3 нема коми перед а
GEN 43:19 нема символу пунктуації на кінці
EXO 12:42 `в роди і роди їх`
EXO 26:3 `калїми` і `келіїми`
EXO 34:22 `держатя меш`
LEV 5:23 `видусив`
LEV 21:1 `не опоганюєть`
NUM 27:20 `достойньства`
NUM 31:46 `людьких`
DEU 17:8 `та`
RUT 4:14 `жінки` замість `жінка`
1SA 30:15 `тото`
1SA 30:15 `горду`
2SA 7:12 `спочнеш` замість `спочинеш`
2SA 8:1 `данини (Гет)`
2SA 19:32 не знак питання на кінці мабуть
1KI 11:41 `Инчі`
1KI 11:41 `Саломонових`
1KI 18:19 `Ізраїляа`
1KI 19:2 `те, саме` зайва кома
1CH 1:32 `(Сини Деданові: Рагуїл, Навдеїл, Ассурим, Летусим, Леюмим (Астусіїм, Асомин).` додано, а в ній додана `(Астусіїм, Асомин)`: прибрати другу дужку відкриваючу
PSA 62:9 Відсутня крапочка на кінці
ISA 41:4 крапочка в кінці
ISA 41:4 має бути не знак питання на кінці
ISA 42:2 `гнівний`
JER 18:13 `таке? (давна) дїва`
MAT 27:43 Слова Ісусові цитуються
MAT 27:63 Ісусові Слова цитуються
MRK 12:28 `пруступивши` замість `приступивши`
ACT 9:22 `у силу та в силу`
HEB 13:17 вони бо **пильнують** душ ваших
1KI 20:29 сто **тисячей** чоловіка
2KI 1:18 книзї **лїстописній** царів
SNG 5:14 тїло **—** його [зайва риска мабуть]
ACT 9:8 Савло **в** землї
EZK 1:14 І **ввихаллись** животини
EZK 4:15 тобі **товарячий** гній
1CH 18:6 скрізь, **киди** він
1CH 22:15 спосібних **ло** всякої
1CH 24:5 й **киязями** Божими
1CH 6:19 Сини **Мераріїиі**: Махлі
DEU 21:3 міста, **пізьмуть** ялівку
DEU 2:24 і **землею** його
ZEC 9:2 Емат **примежнии**, на
ZEC 9:4 Господь **вробить** його
ZEC 9:5 Аскалон **и** здрігнеться
ZEC 9:9 моїми очима **застим**.
ZEC 14:15 язва **побе** конї
EZK 41:2 по **дру-гім** боцї
NUM 14:11 Господь Мойсейов**і. А** докіль [має бути двокрапка мабуть]
DAN 5:13 панотець **мій-царь** привів
HEB 8:5 скин**ю.** „Гледи [зайва крапка мабуть]
'''.strip()
lines=t.split('\n')

Book_names=[]
for file_name in os.listdir(original_folder_path):
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

code_folder_path=os.path.join(root_folder_path,'code')
target_path=os.path.join(code_folder_path,'Table.md')
with open(target_path,encoding='utf-8',mode='w') as f:
    for entry in sorted_entries:
        f.write(f'{entry.Book} {entry.chapter}:{entry.verse}{" " if entry.content else ""}{entry.content}\n')