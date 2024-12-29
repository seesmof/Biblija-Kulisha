# TODO add all the logs to changes and sort changes.csv
import os
from nicegui import ui,app

from code.Original_Automations import original_folder

def reset_local_storage():
    app.storage.general['Book']=''
    app.storage.general['Chapter']=''
    app.storage.general['Verse']=''
    app.storage.general['Mistake']=''
    app.storage.general['Correction']=''
    app.storage.general['Reason']=''

def add_new_change_entry(changes_file_path: str):
    if app.storage.general['Book']=='' or app.storage.general['Chapter']=='' or app.storage.general['Verse']=='' or app.storage.general['Mistake']=='' or app.storage.general['Correction']=='' or app.storage.general['Reason']=='':
        return
    entry_line=f'| {app.storage.general['Book']} | {app.storage.general['Chapter']} | {app.storage.general['Verse']} | {app.storage.general['Mistake']} | {app.storage.general['Correction']} | {app.storage.general['Reason']} |'

    with open(changes_file_path,encoding='utf-8',mode='a') as f:
        f.write('\n' + entry_line)
    reset_local_storage()

root_folder=os.path.dirname(os.path.abspath(__file__))
changes_file_path=os.path.join(root_folder,'..','docs','Changes.md')
reasons_autocomplete=['wrong','missing','letter','symbol']

Book_names=[]
for file in os.listdir(original_folder):
    Book_names.append(file[2:5])

ui.select(label='Book',options=Book_names,with_input=True,).bind_value(app.storage.general,'Book')
ui.input(label='Chapter').bind_value(app.storage.general,'Chapter')
ui.input(label='Verse').bind_value(app.storage.general,'Verse')
ui.input(label='Mistake').bind_value(app.storage.general,'Mistake')
ui.input(label='Correction').bind_value(app.storage.general,'Correction')
ui.input(label='Reason',autocomplete=reasons_autocomplete,).bind_value(app.storage.general,'Reason')
ui.button('Amen',on_click=lambda: add_new_change_entry(changes_file_path))

ui.run(favicon='🏖️',title='Bible change adder')