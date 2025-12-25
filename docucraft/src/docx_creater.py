"""
Module for generating and saving Word documents from templates using Jinja2 and docxtpl.
"""

from typing import Any, NewType
from collections.abc import Iterator, Callable # noqa: F401
from pathlib import Path

from jinja2.exceptions import UndefinedError
from docxtpl import DocxTemplate # type: ignore

from docucraft.src.logger import logger
from docucraft.src.utils import sanitize_filename
from docucraft.src.jinja_env import get_custom_jinja2_env

FileName = NewType('FileName', str)
type TplContext = dict[str, Any]
type FileContext = dict[FileName, TplContext]


def create_docx_from_tpl(*, tpl: DocxTemplate, output_dir: Path | str, filename: FileName, context: TplContext) -> None:
    """Generate and save a Word document by filling in the template with data"""
    output_dir = Path(output_dir)
    output_path = output_dir / f"{sanitize_filename(filename)}.docx"
    try:
        tpl.render(context, jinja_env=get_custom_jinja2_env(log_prefix_msg=filename))
    except UndefinedError:
        logger.exception(f"Ошибка при обработке файла {output_path!r}. Возможно переменная участвует в математических "
                         f"операциях, в таком случае она должна быть явно определена или обработана в шаблоне.")
        raise

    tpl.save(output_path)
    logger.info("%r успешно обработан.", filename)
  

def create_documents_pre() -> None:
    """Check data validity before generating documents"""
    raise NotImplementedError


def create_documents(tpl_path: Path | str, filecontext: FileContext, output: Path) -> int:
    """
    Create .docx from the template and data dictionary and saves it in the specified folder
    Dictionary keys should match the Jinja2 template variables in your .docx file (e.g., {{ title }}, {{ employees }})

    >>> filecontext = {
    ...    '90 GOSSK St': {
    ...        'Laptop': 744.62,
    ...        'Apple': 10.56,
    ...        'table1': [{'key': 'item1', 'value': 1849}]
    ...    },
    ... }

    :param tpl_path: The path to the template in which to replace {{ var }} with data from dict_
    :param filecontext: Data for filling in variables
    :param output: The folder where the finished documents will be stored .docx
    :return: Count of .docx
    """
    count_docx = 0
    logger.info(f"Загрузка шаблона Word из: {tpl_path!r}")
    tpl_path = Path(tpl_path)
    tpl = DocxTemplate(tpl_path)
    tpl_vars = tpl.get_undeclared_template_variables()

    for address, context in filecontext.items():

        if undeclared_variables := context.keys() - tpl_vars:
            logger.info(f"Неиспользованные переменные {address!r}: {undeclared_variables!r}")

        create_docx_from_tpl(
            tpl=tpl,
            context=context,
            output_dir=output,
            filename=address
        )
        count_docx += 1

    logger.info(f"Word документы сохранены в {output!r}, кол-во: {count_docx}")
    return count_docx
