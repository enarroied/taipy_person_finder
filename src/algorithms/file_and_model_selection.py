from pathlib import Path

import pandas as pd

from .similarity_score import RetrieveSimilarNamesForCSV as RetrieveSimilarNamesForCSV
from .similarity_score import (
    RetrieveSimilarNamesForParquet as RetrieveSimilarNamesForParquet,
)


def select_file_type(file_path: str) -> str:
    path_obj = Path(file_path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
    return path_obj.suffix.lower()


def select_runner(
    file_path: str,
) -> RetrieveSimilarNamesForCSV | RetrieveSimilarNamesForParquet:
    file_type = select_file_type(file_path)
    if file_type == ".csv":
        return RetrieveSimilarNamesForCSV()
    if file_type == ".parquet":
        return RetrieveSimilarNamesForParquet()
    else:
        raise f"The file type needs to be csv or parquet, found {file_type}"


def read_data_file(file_path: str) -> pd.DataFrame:
    file_extension = select_file_type(file_path)
    if file_extension == ".csv":
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise IOError(f"Error reading CSV file: {e}")
    elif file_extension == ".parquet":
        try:
            return pd.read_parquet(file_path)
        except Exception as e:
            raise IOError(f"Error reading Parquet file: {e}")
