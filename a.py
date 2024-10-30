import glob
import os 
original=os.path.join(os.path.dirname(os.path.abspath(__file__)),"Original")
print(
    os.listdir(original),glob.glob(original+"\\*.USFM"),
    os.listdir(original)==glob.glob(original+"\\*.USFM")
)