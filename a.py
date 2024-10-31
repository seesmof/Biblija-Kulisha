source=r'\v 14 Тим прозвано криницю ту: "Криницею Живого, що мене бачить." Се між Кадесом і Баредом.'
double_quotes="“ ”"
double_open,double_close=double_quotes.split()
single_quotes="‘ ’"
single_open,single_close=single_quotes.split()

words=[]
opened=False
for word in source.split():
    if '"' in word: 
        opened=not opened
        words.append(word.replace('"',double_open if opened else double_close))
    else: words.append(word)
result=" ".join(words)
print(result)