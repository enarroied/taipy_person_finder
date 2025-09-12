from pathlib import Path

import duckdb
import pandas as pd
from jinja2 import Environment, FileSystemLoader


class QueryRunner:
    """
    Base class to render and execute SQL queries using Jinja2 templates.

    This class provides a reusable interface for loading SQL templates
    from a specified directory, rendering them with parameters, and
    executing the resulting SQL using DuckDB.

    Attributes:
        jinja_env (jinja2.Environment): Environment for loading SQL templates.
        template_dir (Path): Directory containing SQL template files.
    """

    def __init__(self, template_dir: Path | str = None):
        """
        Initialize QueryRunner with a directory for SQL templates.

        Args:
            template_dir (Path | str, optional): Path to SQL template directory.
                Defaults to './sql' relative to this file.
        """
        self.template_dir = Path(
            template_dir or Path(__file__).resolve().parent / "sql"
        )
        self.jinja_env = Environment(loader=FileSystemLoader(self.template_dir))

    def render_query(self, template_name: str, **params) -> str:
        """Creates the query from the template and the provided variables.

        Args:
            template_name (str): name of the SQL template file to create the
            query.

        Raises:
            FileNotFoundError: the file doesn't exist
            ValueError: the template can't render properly

        Returns:
            str: SQL query
        """
        try:
            template = self.jinja_env.get_template(template_name)
        except Exception as e:
            raise FileNotFoundError(
                f"Template '{template_name}' not found in {self.template_dir}"
            ) from e
        try:
            return template.render(**params)
        except Exception as e:
            raise ValueError(
                f"Error rendering template '{template_name}' with \
                    params {params}"
            ) from e

    def execute(self, template_name: str, **params) -> pd.DataFrame:
        """Executes the SQL query

        Args:
            template_name (str): name of the SQL template file to create the
        query.

        Returns:
            pd.DataFrame: SQL query's result
        """
        sql = self.render_query(template_name, **params)
        return duckdb.execute(sql).df()


class RetrieveSimilarNames(QueryRunner):
    """Executes a query to find a single person in the population file using
    jaro-winkler similarity and a threshold value."""

    def run(
        self,
        person_name: str,
        threshold: int,
        data_source: str = "read_parquet('./data/fake_data.parquet')",
    ) -> pd.DataFrame:
        """Execute the jaro_winkler

        Args:
            person_name (str): name of the person to look for
            threshold (int): jaro-winkler threshold value
            data_source (str, optional): Company data to query. Defaults to
        "read_parquet('./data/fake_data.parquet')".

        Returns:
            pd.DataFrame: Result of the SQL query, with all rows of the result.
        """
        name_to_look_for = "".join(person_name.split())
        return self.execute(
            "find_person.sql.j2",
            person_name=name_to_look_for,
            threshold=threshold,
            data_source=data_source,
        )
