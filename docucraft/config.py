from typing import Any

from pydantic_settings import BaseSettings

from pathlib import Path


class Settings(BaseSettings):
    """Class for main settings"""
    _case_sensitive = False

    BASE_DIR: Path = Path(__file__).parent.parent
    PATH_TO_EXCEL: Path = BASE_DIR / 'tests' / 'templates' / 'dummy_excel.xlsx'
    TABLE_NAME_IN_EXCEL: str = 'dummy_data'
    GROUP_BY_COLUMN: str = 'Address'
    PATH_TO_DOCX_TPL: Path = BASE_DIR / 'tests' / 'templates' / 'dummy_doc.docx'
    OUTPUT_DIR_DOCX: Path = BASE_DIR / 'reports'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.OUTPUT_DIR_DOCX.mkdir(parents=True, exist_ok=True)

settings = Settings()
