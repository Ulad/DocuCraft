"""
Module for generating and saving Word documents from templates using Jinja2 and docxtpl.
"""

from typing import Any
from collections.abc import Iterator, Callable # noqa: F401
from pathlib import Path

from jinja2.exceptions import UndefinedError
from docxtpl import DocxTemplate # type: ignore

from docucraft.src.logger import logger
from docucraft.src.utils import sanitize_filename
from docucraft.src.jinja_env import get_custom_jinja2_env


def _process_document(*, template: DocxTemplate, output_dir: Path, document_key: str,
                      context: dict[str, Any]) -> None:
    """Generate and save a Word document by filling in the template with data"""
    output_path = output_dir / f"{sanitize_filename(document_key)}.docx"
    try:
        template.render(context, jinja_env=get_custom_jinja2_env(log_prefix_msg=document_key))
        template.save(output_path)

    except UndefinedError:
        logger.exception(f"Error processing the {output_path!r} file. Perhaps the variable is involved in mathematical "
                         f"operations, in which case it must be explicitly defined or processed in a template.")
        raise
    except:
        logger.exception(f"File processing error {output_path!r}")
        raise
    else:
        logger.info("%r Success", document_key)

def create_documents_pre() -> None:
    """Check data validity before generating documents"""
    raise NotImplementedError


def create_documents(tpl_path: Path,
                     dict_: dict[str, dict[str, str | float | list[dict[str, Any]] | dict[str, Any]]],
                     output: Path) -> int:
    """
    Create .docx from the template and data dictionary and saves it in the specified folder
    'dict_' example_:

    >>> dict_ = {
    ...    '90 GOSSK St': {
    ...        'Laptop': 744.62,
    ...        'Apple': 10.56,
    ...        'table1': [{'key': 'item1', 'value': 1849}]
    ...    },
    ... }

    :param tpl_path: The path to the template in which to replace {{ var }} with data from dict_
    :param dict_: Data for filling in variables
    :param output: The folder where the finished documents will be stored .docx
    :return: Count of .docx
    """
    count_docx = 0
    logger.info(f"Uploading a Word template: {tpl_path.name!r}")
    tpl = DocxTemplate(tpl_path)
    tpl_vars = tpl.get_undeclared_template_variables()
    for key, data in dict_.items():
        undeclared_variables = data.keys() - tpl_vars
        if undeclared_variables:
            logger.info(f"Unused data {key!r:<20}: {undeclared_variables!r}")
        _process_document(
            template=tpl,
            context=data,
            output_dir=output,
            document_key=key
        )
        count_docx += 1

    logger.info(f"Word documents are saved in {output.name!r}, count: {count_docx}")
    return count_docx
