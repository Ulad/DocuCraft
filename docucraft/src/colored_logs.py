from logging import Formatter, LogRecord
from typing import ClassVar


class CustomColoredFormatter(Formatter):
    """Colored output formatter."""
    COLORS: ClassVar = {
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\x1b[31;1m',  # Bold red
        'RESET': '\033[0m'       # Reset color
    }
    def format(self, record: LogRecord) -> str:
        """Format the given log record into a colored string."""
        formatted_message = super().format(record)
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        return f"{level_color}{formatted_message}{self.COLORS['RESET']}"
