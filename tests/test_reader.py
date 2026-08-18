from pathlib import Path

import pytest

from backend.pdf_engine.reader import PDFReader


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = (
    PROJECT_ROOT /
    "sample_files" /
    "test.pdf"
)


def test_pdf_exists():

    assert PDF_PATH.exists()


def test_reader_opens_pdf():

    reader = PDFReader(PDF_PATH)

    assert reader.document is not None

    reader.close()


def test_page_count():

    reader = PDFReader(PDF_PATH)

    assert reader.document.page_count > 0

    reader.close()


def test_invalid_pdf_path():

    missing_path = (
        PROJECT_ROOT /
        "sample_files" /
        "does_not_exist.pdf"
    )

    with pytest.raises(FileNotFoundError):
        PDFReader(missing_path)