from src.algorithms.similarity_score import QueryRunner, RetrieveSimilarNames


def test_render_query_includes_expected_values():
    runner = QueryRunner()
    result = runner.render_query(
        "find_person.sql.j2", person_name="JohnDoe", threshold=0.8
    )
    assert "JohnDoe" in result
    assert "0.8" in result
    assert "jaro_winkler_similarity" in result


def _create_test_data_source(*people):
    """Helper to create test data.
    Usage: _create_test_data_source(('John', 'Doe'), ('Jane', 'Smith'))
    """
    values = ", ".join([f"('{first}', '{last}')" for first, last in people])
    return f"(SELECT * FROM (VALUES {values}) AS test_table(first_name, family_name))"


def test_retrieve_similar_names_high_threshold():
    """Should only find exact/very close matches"""
    test_data = _create_test_data_source(
        ("John", "Doe"), ("Jane", "Smith"), ("Adam", "Johnson")
    )

    retriever = RetrieveSimilarNames()
    result = retriever.run("JohnDoe", 0.9, test_data)

    # Should find John Doe (exact match when spaces removed)
    assert len(result) == 1
    assert result.iloc[0]["first_name"] == "John"
    assert result.iloc[0]["family_name"] == "Doe"


def test_retrieve_similar_names_low_threshold():
    """Test with low threshold - should find multiple matches"""
    test_data = _create_test_data_source(
        ("John", "Doe"),
        ("Jon", "Do"),
        ("Jane", "Smith"),
        ("Xavier", "Zzz"),
    )

    retriever = RetrieveSimilarNames()
    result = retriever.run("JohnDoe", 0.3, test_data)

    assert len(result) >= 2  # John Doe and Jon Do
    # Results should be ordered by similarity (best first)
    assert result.iloc[0]["first_name"] == "John"


def test_retrieve_similar_names_no_matches():
    """Test with no similar names"""
    test_data = _create_test_data_source(("Xavier", "Zzz"), ("Quincy", "Qwerty"))
    retriever = RetrieveSimilarNames()
    result = retriever.run("JohnDoe", 0.5, test_data)

    assert len(result) == 0
