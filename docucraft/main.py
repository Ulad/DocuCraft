"""
Module automates the generation of documents (in .docx) based on input data.
It uses a predefined Word template to create Word documents.
The module handles the entire workflow, including data loading, transformation, document generation.
The process relies on the 'docxtpl' library (https://docxtpl.readthedocs.io/en/latest/), using Jinja2.

The process involves 2 main components:
    1. The template 'file.docx' with placeholders {{ name }} that need to be filled in
    2. Dictionary data:
        key - used as the filename for generated documents
        value - another dictionary where each key corresponds to a placeholder in the template
"""

from docucraft.src.data_loader import read_excel_table
from docucraft.src.docx_creater import create_documents
from docucraft.src.utils import get_peak_memory_usage, log_timeit
from docucraft.src.logger import logger
from docucraft.config import settings as cfg


@log_timeit
def main() -> None:
    """Orchestrates the entire workflow."""
    df_to_dict = read_excel_table(cfg.PATH_TO_EXCEL, table_name=cfg.TABLE_NAME_IN_EXCEL)
    df_to_dict = df_to_dict.rows_by_key(key=cfg.GROUP_BY_COLUMN)
    df_to_dict = {key: dict(value) for key, value in df_to_dict.items()}

    create_documents(cfg.PATH_TO_DOCX_TPL, df_to_dict, cfg.OUTPUT_DIR_DOCX)

    logger.info(get_peak_memory_usage())


if __name__ == "__main__":
    logger.info(cfg.model_dump_json(indent=4))
    main()
