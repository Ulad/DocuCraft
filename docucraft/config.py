"""
Pedantic-settings always tries to determine the values of fields by reading them from environment variables.
By default, the name of the environment variable must match the name of the field.
The default values will still be used if the corresponding environment variable is not set.
Environment variables will always take precedence over the values loaded from the dotenv file.
Documentation: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
"""

from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

BASE_DIR: Path = Path(__file__).parent.parent

class Settings(BaseSettings):
    """Class for main settings"""
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")

    PATH_TO_EXCEL: Path = BASE_DIR / 'tests' / 'templates' / 'dummy_excel.xlsx'
    TABLE_NAME_IN_EXCEL: str = 'dummy_data'
    GROUP_BY_COLUMN: str = 'Address'
    PATH_TO_DOCX_TPL: Path = BASE_DIR / 'tests' / 'templates' / 'dummy_doc.docx'
    OUTPUT_DIR_DOCX: Path = BASE_DIR / 'reports'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.OUTPUT_DIR_DOCX.mkdir(parents=True, exist_ok=True)

settings = Settings()
