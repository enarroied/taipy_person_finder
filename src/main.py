import pandas as pd
from pages import *

from taipy.gui import Gui

tool_pages = {
    "/": root,
    "find_person": find_person_page,
    "find_people": find_people_page,
}

stylekit = {"color_primary": "#DF2D8F", "color_secondary": "#3a3a3a"}

if __name__ == "__main__":
    person_name = ""
    threshold_person = 0.90
    name_type = "Full Name"
    df_similar_person = pd.DataFrame()

    file_for_comparison = None
    df_people_for_comparison = None

    gui = Gui(pages=tool_pages, css_file="./css/main.css")
    gui.run(
        title="Taipy 🔎 Person Finder",
        # favicon="./img/logo.png",
        stylekit=stylekit,
        use_reloader=True,
    )
