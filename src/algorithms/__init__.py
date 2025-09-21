from .file_and_model_selection import DataReaderFactory, FileProcessorFactory
from .similarity_score import RetrieveSimilarNames as RetrieveSimilarNames


# Create convenience functions
def get_columns_dataframe(file_path: str):
    return DataReaderFactory.get_columns_dataframe(file_path)


def get_processor(file_path: str):
    return FileProcessorFactory.get_processor(file_path)
