import taipy.gui.builder as tgb
from taipy.gui import hold_control, notify, resume_control

from algorithms import get_columns_dataframe, get_processor


def _notify_file_failure(state, message):
    with state as s:
        s.show_dataset_selectors = False
        notify(s, "e", message)


def _assert_dataset_has_two_columns(state, dataset_colums):
    if len(dataset_colums) > 1:
        return True
    _notify_file_failure(state, "The dataset needs to have at least 2 columns")
    return False


def _assign_bound_values(state, dataset_colums):
    with state as s:
        s.dataset_colums = dataset_colums
        s.column_first_name = dataset_colums[0]
        s.column_last_name = dataset_colums[1]


def upload_file(state):
    with state as s:
        s.df_similar_people = s.df_similar_people.head(0)
        try:
            people_for_comparison = get_columns_dataframe(s.file_for_comparison)
        except Exception:
            _notify_file_failure(s, "The file can't be read.")
            return

        dataset_colums = list(people_for_comparison.columns)
        if _assert_dataset_has_two_columns(s, dataset_colums):
            s.show_dataset_selectors = True
            _assign_bound_values(s, dataset_colums)


def look_for_similar_people(state):
    with state as s:
        hold_control(s, message="Lookig for Similar People")
        runner = get_processor(s.file_for_comparison)
        df_similar_people = runner.run(
            data_for_comparison=s.file_for_comparison,
            comparison_first_name=s.column_first_name,
            comparison_family_name=s.column_last_name,
            threshold=s.threshold_people,
        )
        df_similar_people["jaro_winkler_similarity_score"] = df_similar_people[
            "jaro_winkler_similarity_score"
        ].round(2)
        s.df_similar_people = df_similar_people
        resume_control(s)


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
