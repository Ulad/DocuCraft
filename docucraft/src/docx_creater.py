"""
Module for generating and saving Word documents from templates using Jinja2 and docxtpl.
"""

from pathlib import Path

from pydantic import TypeAdapter, ConfigDict
from docxtpl import DocxTemplate # type: ignore

from docucraft.src.logger import logger
from docucraft.src.jinja_env import get_custom_jinja2_env
from docucraft.src.custom_types import FilesDict, JinjaContext

FILES_DICT_ADAPTER: TypeAdapter[FilesDict] = TypeAdapter(FilesDict, config=ConfigDict(arbitrary_types_allowed=True))


def create_document(*, tpl: DocxTemplate, filepath: Path, context: JinjaContext) -> None:
    """Generate and save a Word document by filling in the template with data"""

    tpl.render(context, jinja_env=get_custom_jinja2_env(log_prefix_msg=filepath.name))
    tpl.save(filepath)

    logger.info("%r Success", filepath)


def create_documents_pre(files_dict: FilesDict) -> FilesDict:
    """Check data validity before generating documents"""
    return FILES_DICT_ADAPTER.validate_python(files_dict)


def create_documents(tpl_path: Path | str, files_dict: FilesDict) -> None:
    """
    Create .docx from the template and data dictionary and saves it in the specified folder
    Dictionary keys should match the Jinja2 template variables in your .docx file (e.g., {{ title }}, {{ employees }})

    >>> files_dict = {
    ...     Path('output/report1.docx'): {
    ...        'title': 'Отчет за январь',
    ...        'total': 1_000.50,
    ...        'items': [{'name': 'Item 1', 'value': 100}, {'name': 'Item 2', 'value': 200},]
    ...     }
    ... }
    """
    files_dict = create_documents_pre(files_dict)

    logger.info(f"Uploading a Word template: {tpl_path!r}")
    tpl = DocxTemplate(tpl_path)
    tpl_vars = tpl.get_undeclared_template_variables()

    for filepath, context in files_dict.items():
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if undeclared_variables := context.keys() - tpl_vars:
            logger.info(f"Unused data {filepath!r:<20}: {undeclared_variables!r}")

        create_document(tpl=tpl, context=context, filepath=filepath)
