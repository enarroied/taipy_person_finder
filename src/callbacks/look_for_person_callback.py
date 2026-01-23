from algorithms import RetrieveSimilarNames, normalize_name


def look_for_person(name, threshold_person):
    runner = RetrieveSimilarNames()
    df_similar_person = runner.run(name, threshold_person)
    df_similar_person["jaro_winkler_similarity_score"] = df_similar_person[
        "jaro_winkler_similarity_score"
    ].round(2)
    return df_similar_person


def look_for_person_callback(state):
    with state as s:
        name = normalize_name(s.person_name)
        s.df_similar_person = look_for_person(name, s.threshold_person)
