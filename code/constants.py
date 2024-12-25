import os 

class Constants:
    code_folder_path:str=os.path.dirname(os.path.abspath(__file__))
    root_folder_path:str=os.path.join(code_folder_path,'..')
    original_folder_path:str=os.path.join(root_folder_path,'Original')
