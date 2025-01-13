import subprocess 

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

combined='\u0301'
raw='´'
word='госпо́дї'
word=word[:5]+combined+word[5:]
print(word)
copy2clip(combined)