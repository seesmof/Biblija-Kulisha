# check if Original.txt file exists 
import os

root=os.path.dirname(os.path.abspath(__file__))
target=os.path.join(root,"Original.txt")
with open(target,encoding='utf-8',mode='w+') as f:
    f.writelines(["HALLELUJAH","AMEN"])