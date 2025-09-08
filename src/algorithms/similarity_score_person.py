from pathlib import Path

import duckdb
import pandas as pd
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).resolve().parent / "sql"


class QueryRunner:
    def __init__(self):
        self.jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    def render_query(self, template_name: str, **params) -> str:
        template = self.jinja_env.get_template(template_name)
        return template.render(**params)

    def execute(self, template_name: str, **params) -> pd.DataFrame:
        sql = self.render_query(template_name, **params)
        return duckdb.execute(sql).df()


class RetrieveSimilarNames(QueryRunner):
    def run(
        self,
        person_name: str,
        threshold: float,
        data_source: str = "read_parquet('./data/fake_data.parquet')",
    ) -> pd.DataFrame:
        name_to_look_for = "".join(person_name.split())
        return self.execute(
            "find_person.sql.j2",
            person_name=name_to_look_for,
            threshold=threshold,
            data_source=data_source,
        )
