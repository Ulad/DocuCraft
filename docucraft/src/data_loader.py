"""
Module is responsible for data loading to DataFrame
"""

from pathlib import Path

from polars import DataFrame, read_excel

from docucraft.src import logger


def read_excel_table(excel_path: Path, *, table_name: str) -> DataFrame:
    """
    Load data from Excel named table to the DataFrame
    :param excel_path: Path to a file
    :param table_name: Name of a specific table to read. Note that table names are unique across the workbook
    :return: DataFrame
    """
    df = read_excel(excel_path, table_name=table_name)
    logger.info(f"Loaded Excel table from: {excel_path.name, table_name!r}, shape: {df.shape}")
    logger.info(f"Columns: {df.columns!r}")
    if df.null_count().sum_horizontal().sum():
        logger.warning(f"There is nulls in the data: {df.null_count().to_dict(as_series=False)}")
    return df
