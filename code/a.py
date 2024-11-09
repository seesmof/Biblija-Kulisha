import glob
import os


root=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
original_folder_path=os.path.join(root,"Original")
original_file_paths=glob.glob(original_folder_path+"\\*.USFM")

a=[]