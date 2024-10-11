import os
a=[]
for n in range(1,67): a.append(f"0{n}" if n<10 else n)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Perevireni Knygy.md"), "w",encoding="utf-8") as f:
    for n in a:
        f.write(f"{n}\n")