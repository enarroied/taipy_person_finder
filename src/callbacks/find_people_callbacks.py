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
