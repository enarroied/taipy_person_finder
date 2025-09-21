from pathlib import Path
from typing import Type

import pandas as pd

from .similarity_score import (
    RetrieveSimilarNamesForCSV,
    RetrieveSimilarNamesForFile,
    RetrieveSimilarNamesForParquet,
)


class FileProcessorFactory:
    _processors: dict[str, Type[RetrieveSimilarNamesForFile]] = {
        ".csv": RetrieveSimilarNamesForCSV,
        ".parquet": RetrieveSimilarNamesForParquet,
    }

    @classmethod
    def register_processor(
        cls, extension: str, processor: Type[RetrieveSimilarNamesForFile]
    ) -> None:
        """Register a new file processor for a given extension."""
        cls._processors[extension.lower()] = processor

    @classmethod
    def get_processor(cls, file_path: str) -> RetrieveSimilarNamesForFile:
        """Get the appropriate processor for the given file path."""
        file_extension = cls._get_file_extension(file_path)
        processor_class = cls._processors.get(file_extension)
        if processor_class is None:
            raise ValueError(
                f"The file type needs to be csv or parquet, found {file_extension}"
            )
        return processor_class()

    @staticmethod
    def _get_file_extension(file_path: str) -> str:
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
        return path_obj.suffix.lower()


class DataReaderFactory:
    _readers: dict[str, callable] = {
        ".csv": pd.read_csv,
        ".parquet": pd.read_parquet,
    }

    @classmethod
    def register_reader(cls, extension: str, reader: callable) -> None:
        """Register a new data reader for a given extension."""
        cls._readers[extension.lower()] = reader

    @classmethod
    def read_data(cls, file_path: str) -> pd.DataFrame:
        """Read data from a file into a DataFrame."""
        file_extension = cls._get_file_extension(file_path)
        reader = cls._readers.get(file_extension)
        if reader is None:
            raise ValueError(
                f"The file type needs to be csv or parquet, found {file_extension}"
            )
        try:
            return reader(file_path)
        except Exception as e:
            raise IOError(f"Error reading {file_extension} file: {e}")

    @staticmethod
    def _get_file_extension(file_path: str) -> str:
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
        return path_obj.suffix.lower()
