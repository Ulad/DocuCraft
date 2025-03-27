"""
Module for generating and saving Word documents from templates using Jinja2 and docxtpl.
"""

from typing import Any, NoReturn
from collections.abc import Iterator, Callable # noqa: F401
from pathlib import Path
from locale import setlocale, LC_ALL
from logging import Logger

from jinja2 import Environment, Undefined
from jinja2.exceptions import UndefinedError
from docxtpl import DocxTemplate # type: ignore

from docucraft.src.logger import logger
from docucraft.src.utils import sanitize_filename


def _get_custom_jinja2_env(*, prefix_msg: str | None=None, logger: Logger) -> Environment:
    """
    Prepare the environment for Jinja2, which implements custom logging and ignores Undefined objects
    (by default, Jinja2 returns an error). You don't have to use this feature, simply don't specify 'jinja_env'
    parameter in the 'template.render'
    """

    def _log_message(undef: Undefined) -> None:
        """Define a message if an Undefined object is encountered."""
        if prefix_msg:
            logger.warning(f"Template variable warning {prefix_msg!r:<40}: {undef._undefined_message}, ignoring.")
        else:
            logger.warning("Template variable warning: %s", undef._undefined_message)

    class SilentLoggingUndefined(Undefined):
        """
        Whenever the engine cannot find the name of a template variable in the data, it returns an Undefined object.
        The class redefines the behavior of the engine so that with SOME mathematical operations, Undefined
        is simply ignored, and the program does not crash with the jinja2.exceptions error.Undefined Error.
        A logging system for ALL undefined variables is also implemented.
        An example of the old behavior:

        >>> spam = Undefined(name='spam')
        >>> spam + 42
        Traceback (most recent call last):
          ...
        jinja2.exceptions.UndefinedError: 'spam' is undefined

        An example of the new behavior:

        >>> spam = Undefined(name='spam')
        >>> spam + 42
        42
        """
        __slots__ = ()
        __add__ = __radd__ = __sub__ = __rsub__ = \
        __mul__ = __rmul__ = __div__ = __rdiv__ = lambda self, other: other # type: Callable[[Any, Any], Any]

        def _fail_with_undefined_error(self, *args: Any, **kwargs: Any)  -> NoReturn:
            _log_message(self)
            super()._fail_with_undefined_error(*args, **kwargs)

        def __str__(self) -> str:
            _log_message(self)
            return super().__str__()

        def __iter__(self) -> Iterator[Any]:
            _log_message(self)
            return super().__iter__()

        def __bool__(self) -> bool:
            _log_message(self)
            return super().__bool__()


    def f(value: float) -> str:
        """Format a rounded number with spaces between the thousandths"""
        setlocale(LC_ALL, '')  # This will display numbers with spaces between the thousandths.
        return f"{int(round(value, 0)):n}" if value else "0"

    env = Environment(undefined=SilentLoggingUndefined, autoescape=True)
    env.globals.update(f=f)
    return env


def _process_document(*, template: DocxTemplate, output_dir: Path, document_key: str,
                      context: dict[str, Any], prefix_msg_in_log: str) -> None:
    """Generate and save a Word document by filling in the template with data"""
    output_path = output_dir / f"{sanitize_filename(document_key)}.docx"
    try:
        template.render(context, jinja_env=_get_custom_jinja2_env(prefix_msg=prefix_msg_in_log, logger=logger))
        template.save(output_path)

    except UndefinedError:
        logger.exception(f"Error processing the {output_path!r} file. Perhaps the variable is involved in mathematical "
                         f"operations, in which case it must be explicitly defined or processed in a template.")
        raise
    except:
        logger.exception(f"File processing error {output_path!r}")
        raise
    else:
        logger.info("%r успешно обработан.", document_key)


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
            document_key=key,
            prefix_msg_in_log=key
        )
        count_docx += 1

    logger.info(f"Word documents are saved in {output.name!r}, count: {count_docx}")
    return count_docx
