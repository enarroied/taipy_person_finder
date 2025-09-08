from src.algorithms.similarity_score_person import QueryRunner


def test_render_query_includes_expected_values():
    runner = QueryRunner()
    result = runner.render_query(
        "find_person.sql.j2", person_name="JohnDoe", threshold=0.8
    )
    assert "JohnDoe" in result
    assert "0.8" in result
    assert "jaro_winkler_similarity" in result
