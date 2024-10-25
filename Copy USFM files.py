import os
from shutil import copy2
fajly=os.path.join(os.path.dirname(os.path.abspath(__file__)),"Original")
projekt=os.path.join("C:\\My Paratext 9 Projects\\BKS")
for f in os.listdir(fajly): copy2(os.path.join(fajly,f),os.path.join(projekt,f))