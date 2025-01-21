# Original (Біблія Куліша)

- [x] Copy all 66 Books from Bolls.Life into USFM
- [x] Check files integrity: compare chapters with original first and last words; check chapter numbers
- [x] Place each tag on new line
- [x] Replace `'` with `ʼ`
- [x] Replace ` -` with ` —`
- [x] Replace `" "` with `„ ‟`
- [x] Add F tags for footnotes from BIBLE Scans
- [x] Align all `toc1` tags with tables of content. For OT page 12, for NT page 837
- [x] Align running header `h`
- [x] Align Book Book intros `mt`
- [x] Keep `toc2` as they are, orient on the `toc1` and just use shorter versions of that, because translators used different Bible Book abbreviations when referencing them in footnotes.
- [ ] Proofread each verse, align everything with the scan

# Revision (Біблія свободи)

- [x] Copy Original folder, rename to Revision
- [ ] Remove all formatting tags from Original using `\\(\+*)(wj|qt|nd)(\s|\*)`
- [ ] Remove all footnotes from Revision using `\\f(.*?)\\f\*`
- [ ] Update Book names for each
- [ ] Add paragraph tags from WEB
- [ ] Change quotes to corner (squared) ones, add all from WEB
- [ ] Add WJ and ND tags from KJV Authorized Version

Ideas:

- Public domain from start to finish and forever
- Literal translation, so that when translated backwards (Ukrainian to English) it gives the KJV verse approximately (by meaning exactly). Translate all the phrases literally
- Not adding apostrophes nor dashes in words
- Punctuation as in the KJV, no changes
- Formatting tags and words' capitalizaiton (except 'i' not in the beginning of sentence) exactly as in the KJV
- Translate names as clearly as possible, avoid transliteration when an understandable Ukrainian alternative can be found
- Handle all verses with no punctuation sign at the end
