import taipy.gui.builder as tgb

from algorithms import RetrieveSimilarNames, normalize_name


def look_for_person(state):
    runner = RetrieveSimilarNames()
    with state as s:
        name = normalize_name(s.person_name)
        df_similar_person = runner.run(name, s.threshold_person)
        df_similar_person["jaro_winkler_similarity_score"] = df_similar_person[
            "jaro_winkler_similarity_score"
        ].round(2)
        s.df_similar_person = df_similar_person


with tgb.Page() as find_person_page:
    tgb.text("## Find **Person** in Database", mode="md", class_name="color-primary")
    with tgb.layout("4 1"):
        tgb.input("{person_name}", label="Person Name", class_name="fullwidth")
        tgb.slider(
            "{threshold_person}",
            min=0.8,
            max=1,
            step=0.05,
            continuous=False,
            hover_text="Threshold for Jaro-Winkler Score",
        )
    tgb.button(
        "Look for Person", on_action=look_for_person, class_name="fullwidth plain"
    )

    with tgb.part():
        tgb.table("{df_similar_person}", rebuild=True, downloadable=True, filter=True)
