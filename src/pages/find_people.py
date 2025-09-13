from pathlib import Path

import pandas as pd
from algorithms import RetrieveSimilarNamesForCSV, RetrieveSimilarNamesForParquet

import taipy.gui.builder as tgb
from taipy.gui import hold_control, notify, resume_control


def select_file_type(file_path: str) -> str:
    path_obj = Path(file_path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
    return path_obj.suffix.lower()


def select_runner(
    file_path: str,
) -> RetrieveSimilarNamesForCSV | RetrieveSimilarNamesForParquet:
    file_type = select_file_type(file_path)
    if file_type == ".csv":
        return RetrieveSimilarNamesForCSV()
    if file_type == ".parquet":
        return RetrieveSimilarNamesForParquet()
    else:
        raise f"The file type needs to be csv or parquet, found {file_type}"


def read_data_file(file_path: str) -> pd.DataFrame:
    file_extension = select_file_type(file_path)
    if file_extension == ".csv":
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise IOError(f"Error reading CSV file: {e}")
    elif file_extension == ".parquet":
        try:
            return pd.read_parquet(file_path)
        except Exception as e:
            raise IOError(f"Error reading Parquet file: {e}")


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
        try:
            people_for_comparison = read_data_file(s.file_for_comparison)
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
        runner = select_runner(s.file_for_comparison)
        s.df_similar_people = runner.run(
            data_for_comparison=s.file_for_comparison,
            comparison_first_name=s.column_first_name,
            comparison_family_name=s.column_last_name,
            threshold=s.threshold_people,
        )
        print(s.df_similar_person.head())
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
        with tgb.layout("1 1 1"):
            tgb.selector("{column_first_name}", lov="{dataset_colums}", dropdown=True)
            tgb.selector("{column_last_name}", lov="{dataset_colums}", dropdown=True)
            tgb.button(
                label="Find People",
                on_action=look_for_similar_people,
                class_name="fullwidth plain",
            )

        tgb.table("{df_similar_people}", rebuild=True, downloadable=True)
