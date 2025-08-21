import taipy.gui.builder as tgb


def look_for_person(state):
    pass


with tgb.Page() as find_person_page:
    tgb.text("## Find **Person** in Database", mode="md", class_name="color-primary")
    with tgb.layout("4 1 1"):
        tgb.input("{person_name}", label="Person Name", class_name="fullwidth")
        tgb.slider(
            "{threshold_person}",
            min=0.8,
            max=1,
            step=0.05,
            continuous=False,
            hover_text="Threshold for Jaro-Winkler Score",
        )
        tgb.toggle("{name_type}", lov=["First Name", "Full Name"])
    tgb.button(
        "Look for Person", on_action=look_for_person, class_name="fullwidth plain"
    )
