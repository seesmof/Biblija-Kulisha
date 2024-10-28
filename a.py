import re 

a=r"\v 15 І пробував там аж до смерти Іродової, щоб справдилось, що сказав Господь через пророка, глаголючи: \qt Із Єгипту покликав я сина мого.\qt* \v 16 Бачивши тодї Ірод, що мудрцї насьміялись із него, розлютував ся вельми, та й послав повбивати всїх дїтей у Витлеємі й у всїх границях його, од двох років і меньше, по тому часу, що про него він пильно довідував ся в мудрцїв."
a=a.replace("\\wj*","").replace("\\wj ","").replace("\\v ","")
quote:bool=False
words=[]
for word in a.split():
    if word=='\\qt': quote=True
    words.append(word.upper() if quote else word)
    if '\\qt*' in word: quote=False
a=" ".join(words)
a=a.replace("\\QT*","").replace("\\QT ","")

def handle_quotes(verse:str):
    quote:bool=False
    words=[]
    for word in verse.split():
        if word=='\\qt': quote=True
        words.append(word.upper() if quote else word)
        if '\\qt*' in word: quote=False
    return " ".join(words).replace("\\QT*","").replace("\\QT ","")
print(handle_quotes(a)) 