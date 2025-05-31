from typing import Any, Never
from collections.abc import Callable, Iterator  # noqa: F401

from jinja2 import Environment, Undefined

from docucraft.src.logger import logger


class SilentLoggingUndefined(Undefined):
    """
    Class for overriding the standard Jinja2 behavior when encountering an undefined variable.
    - Logs a warning when trying to access an undefined variable.
    - Allows some arithmetic operations (+, -, *, /) to continue by returning another operand.
    attention: This can hide errors if a numeric value (for example, 0) was expected from an undefined variable.
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
    prefix_msg = ''

    __add__ = __radd__ = __sub__ = __rsub__ = \
    __mul__ = __rmul__ = __div__ = __rdiv__ = lambda self, other: other  # type: Callable[[Any, Any], Any]

    def _log_message(self) -> None:
        """Define a message if an Undefined object is encountered."""
        logger.warning("Template variable warning %s: %s, ignoring.", self.prefix_msg, self._undefined_message)

    def _fail_with_undefined_error(self, *args: Any, **kwargs: Any) -> Never:
        self._log_message()
        super()._fail_with_undefined_error(*args, **kwargs)

    def __str__(self) -> str:
        self._log_message()
        return super().__str__()

    def __iter__(self) -> Iterator[Any]:
        self._log_message()
        return super().__iter__()

    def __bool__(self) -> bool:
        self._log_message()
        return super().__bool__()


def f(value: float) -> str:
    """Format a rounded number with spaces between the thousandths"""
    return f'{value:_.0f}'.replace('_', ' ') if value else "0"


def get_custom_jinja2_env(*, log_prefix_msg: str='') -> Environment:
    """Prepare the environment for Jinja2, which implements custom logging and ignores Undefined objects"""
    env = Environment(undefined=SilentLoggingUndefined, autoescape=True)
    env.globals.update(f=f)
    SilentLoggingUndefined.prefix_msg = log_prefix_msg
    return env
