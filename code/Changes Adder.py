# TODO add all the logs to changes and sort changes.csv
import os
from Automations import Ukrainian_Bible_Book_name_to_English_abbrevation
from nicegui import ui, app


def reset_local_storage():
    app.storage.general["Book"] = ""
    app.storage.general["Chapter"] = ""
    app.storage.general["Verse"] = ""
    app.storage.general["Mistake"] = ""
    app.storage.general["Correction"] = ""
    app.storage.general["Reason"] = ""


def add_new_change_entry(changes_file_path: str):
    if (
        app.storage.general["Book"] == ""
        or app.storage.general["Chapter"] == ""
        or app.storage.general["Verse"] == ""
        or app.storage.general["Mistake"] == ""
        or app.storage.general["Correction"] == ""
        or app.storage.general["Reason"] == ""
    ):
        return
    entry_line = f"| {app.storage.general['Book']} | {app.storage.general['Chapter']} | {app.storage.general['Verse']} | {app.storage.general['Mistake']} | {app.storage.general['Correction']} | {app.storage.general['Reason']} |"
    with open(changes_file_path, encoding="utf-8", mode="a") as f:
        f.write("\n" + entry_line)
    reset_local_storage()


root_folder = os.path.dirname(os.path.abspath(__file__))
changes_file_path = os.path.join(root_folder, "..", "docs", "Checks", "Changes.md")
reasons_autocomplete = ["wrong", "missing", "letter", "symbol"]

Book_select = ui.select(
    validation={"Cannot be empty": bool},
    label="Book",
    options=Ukrainian_Bible_Book_name_to_English_abbrevation,
    with_input=True,
).bind_value(app.storage.general, "Book")
Chapter_input = ui.input(
    validation={"Cannot be empty": bool}, label="Chapter"
).bind_value(app.storage.general, "Chapter")
Verse_input = ui.input(validation={"Cannot be empty": bool}, label="Verse").bind_value(
    app.storage.general, "Verse"
)
Mistake_input = ui.input(
    validation={"Cannot be empty": bool}, label="Mistake"
).bind_value(app.storage.general, "Mistake")
Correction_input = ui.input(
    validation={"Cannot be empty": bool}, label="Correction"
).bind_value(app.storage.general, "Correction")
Reason_input = ui.input(
    validation={"Cannot be empty": bool},
    label="Reason",
    autocomplete=reasons_autocomplete,
).bind_value(app.storage.general, "Reason")


class FormValidator:
    def __init__(self, *inputs):
        self.elements = inputs

    @property
    def correct(self):
        return all(
            validation(element.value)
            for element in self.elements
            for validation in element.validation.values()
        )


form_validator = FormValidator(
    Book_select,
    Chapter_input,
    Verse_input,
    Mistake_input,
    Correction_input,
    Reason_input,
)
send_button = ui.button(
    "Make", on_click=lambda: add_new_change_entry(changes_file_path)
).bind_enabled_from(form_validator, "correct")

ui.run(favicon="🏖️", title="Add new Bible change")
