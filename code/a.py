from nicegui import ui

ui.label("AMEN")
ui.button("Greet", on_click=lambda: ui.notify("ALLELUUJAH AND AMEN"))

ui.run(on_air="g20yhJjpodVEVTRb", reload=False)
