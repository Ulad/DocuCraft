from typing import Annotated
from pathlib import Path

from pydantic import StringConstraints
from docxtpl import RichText, Listing, Subdoc, InlineImage # type: ignore

# Only allow alphanumeric and underscores https://jinja.palletsprojects.com/en/stable/api/#notes-on-identifiers
type JinjaTag = Annotated[str, StringConstraints(pattern=r'^[a-zA-Z_][a-zA-Z0-9_]*$')]
type JinjaValue = (
        str | float | None
        | list[JinjaContext]  # For tables
        | JinjaContext  # For nested data
        | list[str]  # For dynamic columns mostly
        | RichText | InlineImage | Subdoc | Listing  # For docxtpl types
)
type JinjaContext = dict[JinjaTag, JinjaValue]
type FilesDict = dict[Path, JinjaContext]
