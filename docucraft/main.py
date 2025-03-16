"""
Module automates the generation of documents (in .docx and .pdf formats) based on input data.
It uses a predefined Word template to create Word documents and (optionally) converts them to PDF.
The module handles the entire workflow, including data loading, transformation, document generation, and conversion.
The process relies on the 'docxtpl' library (https://docxtpl.readthedocs.io/en/latest/), using Jinja2.

The process involves 2 main components:
    1. The template 'file.docx' with placeholders {{ name }} that need to be filled in
    2. Dictionary data:
        key - used as the filename for generated documents
        value - another dictionary where each key corresponds to a placeholder in the template
"""

from docucraft.src.data_loader import read_excel_table
from docucraft.src.utils import get_peak_memory_usage, log_timeit
from docucraft.src import logger
from docucraft.config import settings as cfg


@log_timeit
def main() -> None:
    """Orchestrates the entire workflow."""
    read_excel_table(cfg.PATH_TO_EXCEL, table_name="dummy_data")

    logger.info(get_peak_memory_usage())


if __name__ == "__main__":
    logger.info(cfg.model_dump_json(indent=4, exclude={'BASE_DIR'}))
    main()
