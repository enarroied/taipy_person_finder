from algorithms import RetrieveSimilarNames, normalize_name


def look_for_person_callback(state):
    runner = RetrieveSimilarNames()
    with state as s:
        name = normalize_name(s.person_name)
        df_similar_person = runner.run(name, s.threshold_person)
        df_similar_person["jaro_winkler_similarity_score"] = df_similar_person[
            "jaro_winkler_similarity_score"
        ].round(2)
        s.df_similar_person = df_similar_person
