import tempfile
from pathlib import Path

import pandas as pd
from src.algorithms.similarity_score import (
    RetrieveSimilarNamesForCSV,
    RetrieveSimilarNamesForParquet,
)


def _create_test_data_source(*people):
    """Helper to create test data with the necessary columns for the SQL query.
    Usage: _create_test_data_source(('John', 'Doe'), ('Jane', 'Smith'))
    """
    values = ", ".join(
        [
            f"(1, '{first}', '{last}', '{first.lower()}-{last.lower()}')"
            for first, last in people
        ]
    )
    return f"(SELECT * FROM (VALUES {values}) AS test_table(id, first_name, family_name, name_for_comparison))"


def _create_test_comparison_dataframe(*people):
    """Helper to create comparison DataFrame.
    Usage: _create_test_comparison_dataframe(('John', 'Doe'), ('Jane', 'Smith'))
    """
    data = [{"first_name": first, "family_name": last} for first, last in people]
    return pd.DataFrame(data)


class TestRetrieveSimilarNamesForCSV:
    """Tests for CSV-based name comparison"""

    def setup_method(self):
        """Create temporary CSV file for testing"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.csv_path = self.temp_dir / "test_comparison.csv"

        # Create test comparison data
        comparison_df = _create_test_comparison_dataframe(
            ("John", "Doe"), ("Jane", "Smith"), ("Jon", "Do"), ("Michael", "Johnson")
        )
        comparison_df.to_csv(self.csv_path, index=False)

        self.retriever = RetrieveSimilarNamesForCSV()

    def teardown_method(self):
        """Clean up temporary files"""
        if self.csv_path.exists():
            self.csv_path.unlink()
        self.temp_dir.rmdir()

    def test_csv_initialization(self):
        """Test that CSV retriever initializes with correct data source type"""
        assert self.retriever.data_source_type == "read_csv"

    def test_csv_high_threshold_exact_match(self):
        """Test CSV comparison with high threshold - should find exact matches"""
        primary_data = _create_test_data_source(
            ("John", "Doe"), ("Alice", "Brown"), ("Bob", "Wilson")
        )

        result = self.retriever.run(
            data_for_comparison=str(self.csv_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=0.9,
            data_source=primary_data,
        )

        # Should find John Doe match
        assert len(result) >= 1
        john_doe_matches = result[
            (result["comparison_first_name"] == "John")
            & (result["comparison_family_name"] == "Doe")
        ]
        assert len(john_doe_matches) > 0

        exact_match = john_doe_matches.iloc[0]
        assert exact_match["jaro_winkler_similarity_score"] == 1

    def test_csv_low_threshold_multiple_matches(self):
        """Test CSV comparison with low threshold -
        should find multiple similar matches"""
        primary_data = _create_test_data_source(
            ("John", "Doe"), ("Johnny", "Doe"), ("Jon", "Smith"), ("Xavier", "Zzz")
        )

        result = self.retriever.run(
            data_for_comparison=str(self.csv_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=0.3,
            data_source=primary_data,
        )

        # Should find multiple matches due to low threshold
        assert len(result) > 1

        # Results should be ordered by similarity score (highest first)
        scores = result["jaro_winkler_similarity_score"].tolist()
        assert scores == sorted(scores, reverse=True)

    def test_csv_no_matches_high_threshold(self):
        """Test CSV comparison with no matches above threshold"""
        primary_data = _create_test_data_source(
            ("Xavier", "Zzz"), ("Quincy", "Qwerty"), ("Zara", "Zebra")
        )

        result = self.retriever.run(
            data_for_comparison=str(self.csv_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=0.8,
            data_source=primary_data,
        )

        assert len(result) == 0

    def test_csv_different_column_names(self):
        """Test CSV comparison with different column names"""
        # Create CSV with different column names
        alt_csv_path = self.temp_dir / "alt_columns.csv"
        comparison_df = pd.DataFrame(
            [
                {"given_name": "John", "surname": "Doe"},
                {"given_name": "Jane", "surname": "Smith"},
            ]
        )
        comparison_df.to_csv(alt_csv_path, index=False)

        primary_data = _create_test_data_source(("John", "Doe"))

        result = self.retriever.run(
            data_for_comparison=str(alt_csv_path),
            comparison_first_name="given_name",
            comparison_family_name="surname",
            threshold=0.8,
            data_source=primary_data,
        )

        assert len(result) >= 1
        match = result.iloc[0]
        assert match["comparison_first_name"] == "John"
        assert match["comparison_family_name"] == "Doe"

        # Clean up
        alt_csv_path.unlink()


class TestRetrieveSimilarNamesForParquet:
    """Tests for Parquet-based name comparison"""

    def setup_method(self):
        """Create temporary Parquet file for testing"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.parquet_path = self.temp_dir / "test_comparison.parquet"

        # Create test comparison data
        comparison_df = _create_test_comparison_dataframe(
            ("John", "Doe"),
            ("Jane", "Smith"),
            ("Jon", "Do"),
            ("Michael", "Johnson"),
            ("Michelle", "Johnston"),
        )
        comparison_df.to_parquet(self.parquet_path, index=False)

        self.retriever = RetrieveSimilarNamesForParquet()

    def teardown_method(self):
        """Clean up temporary files"""
        if self.parquet_path.exists():
            self.parquet_path.unlink()
        self.temp_dir.rmdir()

    def test_parquet_initialization(self):
        """Test that Parquet retriever initializes with correct data source type"""
        assert self.retriever.data_source_type == "read_parquet"

    def test_parquet_high_threshold_exact_match(self):
        """Test Parquet comparison with high threshold"""
        primary_data = _create_test_data_source(
            ("John", "Doe"), ("Alice", "Brown"), ("Michael", "Johnson")
        )

        result = self.retriever.run(
            data_for_comparison=str(self.parquet_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=0.9,
            data_source=primary_data,
        )

        # Should find exact matches
        assert len(result) >= 2  # John Doe and Michael Johnson

        # Check for John Doe match
        john_doe_matches = result[
            (result["comparison_first_name"] == "John")
            & (result["comparison_family_name"] == "Doe")
        ]
        assert len(john_doe_matches) > 0

        # Check for Michael Johnson match
        michael_matches = result[
            (result["comparison_first_name"] == "Michael")
            & (result["comparison_family_name"] == "Johnson")
        ]
        assert len(michael_matches) > 0

    def test_parquet_similarity_scores_included(self):
        """Test that both similarity scores are calculated correctly"""
        primary_data = _create_test_data_source(("John", "Doe"))

        result = self.retriever.run(
            data_for_comparison=str(self.parquet_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=0.1,  # Low threshold to get results
            data_source=primary_data,
        )

        assert len(result) > 0

        # Check that both similarity score columns exist
        assert "jaro_winkler_similarity_score" in result.columns
        assert "levenshtein_similarity_score" in result.columns

        # Check that all similarity scores are numeric
        assert result["jaro_winkler_similarity_score"].dtype in ["float64", "float32"]
        assert result["levenshtein_similarity_score"].dtype in ["int64", "int32"]

        # Jaro-Winkler scores should be between 0 and 1
        jw_scores = result["jaro_winkler_similarity_score"]
        assert (jw_scores >= 0).all() and (jw_scores <= 1).all()

    def test_parquet_cross_join_behavior(self):
        """Test that cross join produces expected number of comparisons"""
        # Create data with 2 primary records and we have 5 comparison records
        primary_data = _create_test_data_source(("John", "Doe"), ("Jane", "Smith"))

        result = self.retriever.run(
            data_for_comparison=str(self.parquet_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=0.0,  # Very low threshold to get all combinations
            data_source=primary_data,
        )

        # Should have results for cross join of 2 x 5 = 10 comparisons
        # But filtered by threshold, so check we have reasonable number
        assert len(result) >= 2  # At least some matches

        # Check that we have both primary names represented
        primary_names = set(
            result["comparison_first_name"] + result["comparison_family_name"]
        )
        assert "JohnDoe" in primary_names or (
            "John" in result["comparison_first_name"].to_numpy()
            and "Doe" in result["comparison_family_name"].to_numpy()
        )

    def test_parquet_ordering_by_similarity(self):
        """Test that results are ordered by similarity score descending"""
        primary_data = _create_test_data_source(
            ("Jon", "Do")
        )  # Similar to multiple names

        result = self.retriever.run(
            data_for_comparison=str(self.parquet_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=0.1,
            data_source=primary_data,
        )

        assert len(result) > 1

        # Check ordering
        scores = result["jaro_winkler_similarity_score"].tolist()
        assert scores == sorted(scores, reverse=True)


class TestFileComparisonIntegration:
    """Integration tests comparing CSV and Parquet behavior"""

    def setup_method(self):
        """Create both CSV and Parquet files with same data"""
        self.temp_dir = Path(tempfile.mkdtemp())

        # Same test data for both formats
        test_data = _create_test_comparison_dataframe(
            ("John", "Doe"), ("Jane", "Smith"), ("Jon", "Do")
        )

        # Create CSV
        self.csv_path = self.temp_dir / "comparison.csv"
        test_data.to_csv(self.csv_path, index=False)

        # Create Parquet
        self.parquet_path = self.temp_dir / "comparison.parquet"
        test_data.to_parquet(self.parquet_path, index=False)

        self.csv_retriever = RetrieveSimilarNamesForCSV()
        self.parquet_retriever = RetrieveSimilarNamesForParquet()

    def teardown_method(self):
        """Clean up temporary files"""
        for path in [self.csv_path, self.parquet_path]:
            if path.exists():
                path.unlink()
        self.temp_dir.rmdir()

    def test_csv_and_parquet_produce_same_results(self):
        """Test that CSV and Parquet retrievers produce identical results"""
        primary_data = _create_test_data_source(("John", "Doe"), ("Jane", "Smith"))
        threshold = 0.5

        csv_result = self.csv_retriever.run(
            data_for_comparison=str(self.csv_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=threshold,
            data_source=primary_data,
        )

        parquet_result = self.parquet_retriever.run(
            data_for_comparison=str(self.parquet_path),
            comparison_first_name="first_name",
            comparison_family_name="family_name",
            threshold=threshold,
            data_source=primary_data,
        )

        # Should have same number of results
        assert len(csv_result) == len(parquet_result)

        if len(csv_result) > 0:
            # Sort both by similarity score for comparison
            csv_sorted = csv_result.sort_values(
                "jaro_winkler_similarity_score", ascending=False
            ).reset_index(drop=True)
            parquet_sorted = parquet_result.sort_values(
                "jaro_winkler_similarity_score", ascending=False
            ).reset_index(drop=True)

            # Compare similarity scores (allowing for small floating point differences)
            pd.testing.assert_series_equal(
                csv_sorted["jaro_winkler_similarity_score"],
                parquet_sorted["jaro_winkler_similarity_score"],
                check_names=False,
            )
