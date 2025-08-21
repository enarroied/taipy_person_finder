import taipy.gui.builder as tgb

with tgb.Page() as find_people_page:
    tgb.text(
        "## Find **People** from a File in the Database",
        mode="md",
        class_name="color-primary",
    )
