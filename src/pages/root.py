import taipy.gui.builder as tgb

with tgb.Page() as root:
    with tgb.layout("4 1 1"):
        tgb.text("# Taipy 🔎 Person Finder", mode="md", class_name="color-primary")
        tgb.navbar()
        tgb.toggle(theme=True)
