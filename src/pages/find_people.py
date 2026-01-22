import taipy.gui.builder as tgb
from callbacks.find_people_callbacks import look_for_similar_people, upload_file

with tgb.Page() as find_people_page:
    tgb.text(
        "## Find **People** from a File in the Database",
        mode="md",
        class_name="color-primary",
    )
    tgb.file_selector(
        "{file_for_comparison}",
        label="Upload File",
        on_action=upload_file,
        extensions=".csv, .parquet",
        class_name="fullwidth",
        notify=False,
    )
    with tgb.part(render="{show_dataset_selectors}"):
        tgb.text(
            "## Select Dataset's **First and Last Name**",
            mode="md",
            class_name="color-primary",
        )
        tgb.text(
            """The app will merge first and last name to compare to company data.
             Your dataset needs to have a first and last name column. Select them
             below, along with the similarity threshold:
             """,
            mode="md",
            class_name="color-primary",
        )
        with tgb.layout("1 1 1"):
            tgb.selector(
                "{column_first_name}",
                lov="{dataset_colums}",
                dropdown=True,
                label="First Name",
            )
            tgb.selector(
                "{column_last_name}",
                lov="{dataset_colums}",
                dropdown=True,
                label="Last Name",
            )
            tgb.slider(
                "{threshold_people}",
                min=0.8,
                max=1,
                step=0.05,
                continuous=False,
                hover_text="Threshold for Jaro-Winkler Score",
            )

        tgb.button(
            label="Find People",
            on_action=look_for_similar_people,
            class_name="fullwidth plain",
        )

        tgb.table("{df_similar_people}", rebuild=True, downloadable=True)
