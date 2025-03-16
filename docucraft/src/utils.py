from docucraft.src import logger
from collections.abc import Callable
from timeit import default_timer
from typing import Any, TypeVar, cast
from platform import system

from psutil import Process

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

    for char in invalid_chars:
        if char in filename:
            filename = filename.replace(char, replace_char)
    return filename.strip(". ")


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
