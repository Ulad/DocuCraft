from docxtpl import DocxTemplate
from docx2txt import process

from pathlib import Path

from docucraft.src.docx_creater import create_document

BASE_DIR = Path(__file__).parent / 'templates'


def test_process_document(tmp_path: Path) -> None:
    """
    Compare generated .docx with an extracted .docx file.
    Compares entire text content as a single string.
    This method is straightforward but ignores images, charts, and formatting.
    To fully compare documents, we would need to use something like a pywin32 library (Win only).
    """
    generated_file = tmp_path / 'dummy_doc_result.docx'
    reference_file = BASE_DIR / 'dummy_doc_result.docx'
    template_file = DocxTemplate(BASE_DIR / 'dummy_doc.docx')

    create_document(
        tpl=template_file,
        filepath=generated_file,
        context={"Sofa": 10, "Chair": 0}
    )

    text1 = process(generated_file).replace('\n', '')
    text2 = process(reference_file).replace('\n', '')

    assert generated_file.exists()
    assert text1 == text2
