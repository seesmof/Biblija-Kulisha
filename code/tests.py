from dataclasses import dataclass
from utils import utilities as u

class TestUtilities:
    @staticmethod
    def test_formatting_remover():
        test_cases=[
            (
                r'\v 31 \wj Сказано ж: \+qt Що хто розводить ся з жінкою своєю, нехай дасть їй розвідний лист.\+qt*\wj*',
                r'\v 31 Сказано ж: Що хто розводить ся з жінкою своєю, нехай дасть їй розвідний лист.'
            ),
        ]
        for test_value,expected_output in test_cases:
            assert u.remove_formatting_usfm_tags(test_value)==expected_output
        print('Formatting remover works')

utilities_tester=TestUtilities()

def run():
    utilities_tester.test_formatting_remover()

if __name__=='__main__':
    run()