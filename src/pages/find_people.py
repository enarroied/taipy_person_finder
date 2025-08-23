import pandas as pd

import taipy.gui.builder as tgb


def upload_file(state):
    with state as s:
        df_people_for_comparison = pd.read_csv(s.file_for_comparison)
        print(df_people_for_comparison.columns)


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
        extensions=".csv",
        class_name="fullwidth",
    )
