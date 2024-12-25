import re

class Utilities:
    @staticmethod
    def remove_footnotes_with_text(verse_line):
        footnote_pattern=r'\\(\+*)f(.*?)\\(\+*)f\*'
        return re.sub(footnote_pattern,'',verse_line)
    
    @staticmethod
    def remove_formatting_usfm_tags(verse_line):
        tags_pattern=r'\\(\+*)(wj|qt|nd)(\s|\*)'
        return re.sub(tags_pattern,'',verse_line)

    @staticmethod
    def remove_verse_tags_and_numbers(verse_line):
        verse_tag_and_number_pattern=r'\\v\s\d+\s'
        return re.sub(verse_tag_and_number_pattern,'',verse_line)

utilities=Utilities()

input_verse_line=r'\v 31 \wj Сказано ж: \+qt Що хто розводить ся з жінкою своєю, нехай дасть їй розвідний лист.\+qt*\wj*'
res=utilities.remove_formatting_usfm_tags(input_verse_line)
print(res)