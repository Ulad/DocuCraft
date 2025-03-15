from logging import getLogger
from logging.config import dictConfig
from pathlib import Path

from yaml import safe_load


def setup_logging(config_path: str | Path, log_dir: str | Path="logs") -> None:
    """Create directory for logging, loads config and setup logging"""
    log_dir_path = Path(log_dir).resolve()
    log_dir_path.mkdir(parents=True, exist_ok=True)

    with open(config_path) as f:
        dictConfig(safe_load(f))


setup_logging(config_path=Path(__file__).parent / "log_settings.yaml")
logger = getLogger(__name__)
