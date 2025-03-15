"""
This module automates the generation of documents (in .docx and .pdf formats) based on input data.
It uses a predefined Word template to create Word documents and (optionally) converts them to PDF.
The module handles the entire workflow, including data loading, transformation, document generation, and conversion.
The process relies on the 'docxtpl' library (https://docxtpl.readthedocs.io/en/latest/), using Jinja2.

The process involves 2 main components:
    1. The template 'file.docx' with placeholders {{ name }} that need to be filled in
    2. Dictionary data:
        key - used as the filename for generated documents
        value - another dictionary where each key corresponds to a placeholder in the template
"""


def main() -> None:
    """Orchestrates the entire workflow."""
    print("Hello from docucraft!")


if __name__ == "__main__":
    main()
