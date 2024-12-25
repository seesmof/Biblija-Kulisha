from dataclasses import dataclass
import os 

@dataclass(frozen=True)
class Constants:
    # INTERNAL FOLDER PATHS 
    code_folder_path:str=os.path.dirname(os.path.abspath(__file__))
    root_folder_path:str=os.path.join(code_folder_path,'..')
    original_folder_path:str=os.path.join(root_folder_path,'Original')
    logs_folder_path:str=os.path.join(root_folder_path,'logs')
    tbs_folder_path:str=os.path.join(root_folder_path,'TXT TBS')

    # EXTERNAL FOLDER PATHS 
    paratext_folder_path:str=os.path.join(r'C:\My Paratext 9 Projects\BKS')

constants=Constants()