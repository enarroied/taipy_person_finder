import duckdb
from jinja2 import Template


def retrieve_similar_names(person_name, threshold):
    person_name = "".join(person_name.split())
    sql_template = Template(
        """
    SELECT *,
        jaro_winkler_similarity('{{ person_name }}', first_name || family_name) AS jaro_winkler_similarity_score,
        levenshtein('{{ person_name }}', first_name || family_name) AS levenshtein__similarity_score
    FROM 
        read_parquet('./data/fake_data.parquet')
    WHERE 
        jaro_winkler_similarity_score > {{ threshold }}
    ORDER BY jaro_winkler_similarity_score DESC
    """
    )
    query = sql_template.render(person_name=person_name, threshold=threshold)
    return duckdb.execute(query).df()
