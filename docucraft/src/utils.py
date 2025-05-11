from collections.abc import Callable
from timeit import default_timer
from typing import Any
from platform import system
from functools import wraps
from collections import defaultdict

from psutil import Process

from docucraft.src.logger import logger


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


def log_timeit[T, **P](func: Callable[P, T]) -> Callable[P, T]:
    """Log execution time of a decorated function."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start_time = default_timer()
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__qualname__!r} took: {default_timer() - start_time:.2f} sec.")
        return result
    return wrapper


def merge_dicts[K, V](*dicts: dict[str, dict[K, Any]]) -> dict[str, dict[K, Any]]:
    """
    >>> x = {'90 GOSSK St': {'Laptop': 744.62}, '54 BAZVE St': {'Sofa': 105.84},}
    >>> y = {'90 GOSSK St': {'table': [{'key': 'name1', 'value': 1849}]}}
    >>> result = {
    ...     '54 BAZVE St': {'Sofa': 105.84},
    ...     '90 GOSSK St': {'Laptop': 744.62, 'table': [{'key': 'name1', 'value': 1849}]}
    ... }
    >>> merge_dicts(x, y) == result
    True
    """
    merged: dict[str, dict[K, Any]] = defaultdict(dict)
    for dict_ in dicts:
        for k, v in dict_.items():
            merged[k].update(v)
    return merged
