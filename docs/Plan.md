# Original (Біблія Куліша)

- [x] Copy all 66 Books from Bolls.Life into USFM
- [x] Check files integrity: compare chapters with original first and last words; check chapter numbers
- [x] Place each tag on new line
- [x] Replace `'` with `ʼ`
- [x] Replace ` -` with ` —`
- [x] Replace `" "` with `„ ‟`
- [x] Add F tags for footnotes from BIBLE Scans
- [x] Align all `toc1` tags with tables of content. For OT page 12, for NT page 837
- [ ] Align running header `h`
- [ ] Align Book Book intros `mt`
- [ ] Keep `toc2` as they are, orient on the `toc1` and just use shorter versions of that, because translators used different Bible Book abbreviations when referencing them in footnotes.
- [ ] Proofread each verse, align everything with the scan

# Revision (Біблія свободи)

- [x] Copy Original folder, rename to Revision
- [ ] Remove all formatting tags from Original using `\\(\+*)(wj|qt|nd)(\s|\*)`
- [ ] Remove all footnotes from Revision using `\\f(.*?)\\f\*`
- [ ] Translate each verse literally
- [ ] Add QT tags with F notes with cross-references from [here](https://www.blueletterbible.org/study/misc/quotes.cfm)

Ideas:

- Public domain from start to finish and forever
- Literal translation, so that when translated backwards (Ukrainian to English) it gives the KJV verse approximately (by meaning exactly). Translate all the phrases literally
- Not adding apostrophes nor dashes in words
- Punctuation as in the KJV, no changes
- Formatting tags and words' capitalizaiton (except 'i' not in the beginning of sentence) exactly as in the KJV
- Translate names as clearly as possible, avoid transliteration when an understandable Ukrainian alternative can be found

Known issues in Bible Kulish (Original):

- 1 Мойсея 14 4 `чотирнайцятому` замість `тринайцятому`
- 2 Мойсея 12 42 `в роди і роди їх`
- 3 Мойсея 5 19 `дійсно` замість `існо`
- 5 Мойсея 17 8 `та`
- 5 Мойсея 16 22 verse missing
- 1 Самуїлова 14 42 `.` замість `:`: `І повелїв Саул. Жеребуйте`
- Рути 4 14 `жінки` замість `жінка`
- Псалтирь 58 11 `дійсно` замість `існо`
- Ісаїї 41 4 крапочка в кінці
- Ісаїї 42 2 `гнівний`
- Еремії 18 13 `таке? (давна) дїва`
- Луки 10 22 додати `turning to the disciples, HE said:`
- Луки 13 17 крапочка в кінці: `І, як се промовив, засоромились усї противники Його, а всї люде радувались усїм славним, що сталось від Него?`
- Луки 13 32 `скінчаюся` замість `звершуюся`: `I shall be perfected` (KJV)
- Луки 23 34 додати `diving HIS Garments among them, they cast lots.`
- Йоана 8 58 `Я був` замість `Я Є`: `Before Abraham was, I AM` (KJV)
- Дїяння 9 22 `у силу та в силу`
- 2 Солунян 3 4 переписати `що що`
- Одкриттє 15 6 `лнянку` замість `льняну`
- Одкриттє 17 7 `Длячого` замість `Для чого`
- GEN 9 29 `деватьсот`
- GEN 11 3 нема коми перед а
- ECC 4 5 може не має бути `приговорюючи:`
- JOB 42 11 додати зноску після `кесити`
- 2SA 19 32 не знак питання на кінці мабуть
- Филипян 3 1 радіти безпечно
- Маттея 27 43 Слова Ісусові цитуються
- Маттея 27 63 Ісусові Слова цитуються
- Йоана 7 27
- Йоана 7 36
- Ісаїї 41 4 має бути не знак питання на кінці
- EXO 26 3 `калїми` і `келіїми`
- EXO 34 22 `держатя меш`
- EXO 37 29 `мастиєльників`
- LEV 5 23 `видусив`
- LEV 8 15 `розгрішив`
- LEV 8 36 `Мойсейя`
- LEV 10 17 `ззїли`
- 4 Мойсея 32 9 літера `Э` замість `Є` у `Эсколя`: замінити на `Є`: у друкованій Біблії така літера і є
- 1 Царів 19 2 `те, саме` зайва кома
- Псалтирь 62 9 Відсутня крапочка на кінці
- 1 Паралипоменон 1 32 `(Сини Деданові: Рагуїл, Навдеїл, Ассурим, Летусим, Леюмим (Астусіїм, Асомин).` додано, а в ній додана `(Астусіїм, Асомин)`: прибрати другу дужку відкриваючу
- Дїяння 17 24 `хмарах` замість `храмах`
- Судді 7 1 `Еробаах` замість `Еробаал`
- Йов 27 20 `ва` замість `на`
- Марка 12 28 `пруступивши` замість `приступивши`
- LEV 21 1 `не опоганюєть`
- LEV 22 14 `зʼість`
- NUM 27 20 `достойньства`
- NUM 31 46 `людьких`
- 1SA 18 11 `Давидаʼд`
- 1SA 30 15 `тото`
- 1SA 30 15 `горду`
- 2SA 7 12 `спочнеш` замість `спочинеш`
- 2SA 8 1 `данини (Гет)`
- 1KI 11 41 `Инчі`
- 1KI 11 41 `Саломонових`
- 1KI 18 19 `Ізраїляа`
- GEN 43 19 нема символу пунктуації на кінці
- EST 2 4 `сподоби`
- JOB 13 8 `притворювятись`
- JOB 15 10 `Е й`