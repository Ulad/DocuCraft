from collections.abc import Callable
from timeit import default_timer
from typing import Any, TypeVar, cast
from platform import system
from functools import reduce

from psutil import Process

from docucraft.src.logger import logger

F = TypeVar('F', bound=Callable[..., Any])


def get_peak_memory_usage() -> str:
    """
    Measures the peak amount of RAM used by the process during its execution.
    On Windows, it represents the peak working set size (WSS).
    On Linux, it represents the current resident set size (RSS), as peak usage is not available.
    """
    process = Process().memory_info()

    peak_memory_mb = process.peak_wset // 1024 ** 2 if system() == "Windows" else process.rss // 1024 ** 2

    return f"Peak memory usage: {peak_memory_mb} MiB"


def sanitize_filename(filename: str, replace_char: str = "_") -> str:
    """
    Sanitizes a filename by replacing invalid characters with a specified replacement character.

    >>> sanitize_filename('б-р Загребский, 31/5 лит. А')
    'б-р Загребский, 31_5 лит. А'
    >>> sanitize_filename('б-р Загребский, 31/5 лит. А', '-')
    'б-р Загребский, 31-5 лит. А'

    :param filename: The input filename to sanitize.
    :param replace_char: The character to replace invalid characters with. Default is '_'.
    :return: The sanitized filename.
    """
    invalid_chars = r'[<>:"/\|?*]'
    try:
        for char in invalid_chars:
            if char in filename:
                filename = filename.replace(char, replace_char).strip(". ")
    except TypeError as e:
        logger.error(f"Не удалось обработать {filename!r}, ошибка: {e}")
    return filename


def log_timeit(fnc: F) -> F:
    """
    Measure execution time of a decorated function
    :param fnc: any function.
    :return: function result and prints execution time.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = default_timer()
        result = fnc(*args, **kwargs)
        finish_time = default_timer()
        logger.info(f"Function {fnc.__name__!r} took: {finish_time - start_time:.3f} sec.")
        return result

    return cast(F, wrapper)


def merge_dicts(*dicts: dict[str, Any]) -> dict[str, Any]:
    """
    >>> x = {'90 GOSSK St': {'Laptop': 744.62}, '54 BAZVE St': {'Sofa': 105.84, 'Apple': 686.6},}
    >>> y = {
    ...     '90 GOSSK St': {
    ...         'table': [{'key': 'name1', 'value': 1849},
    ...                   {'key': 'name2', 'value': 18993}]
    ...     },
    ... }
    >>> merge_dicts(x, y)
    {
        '90 GOSSK St': {
            'Laptop': 744.62,
            'table': [{'key': 'name1', 'value': 1849},
                      {'key': 'name2', 'value': 18993}]
        },
        '54 BAZVE St': {'Sofa': 105.84, 'Apple': 686.6},
    }
    """
    return {
        k: reduce(lambda x, y: x | y, [d.get(k, {}) for d in dicts])
        for k in {k for d in dicts for k in d}
    }
