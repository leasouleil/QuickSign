from pathlib import Path

import pytest

from backend.pdf_engine.signer import PDFSigner


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = (
    PROJECT_ROOT /
    "sample_files" /
    "test.pdf"
)

SIGNATURE_PATH = (
    PROJECT_ROOT /
    "sample_files" /
    "signaturetest.png"
)


def test_signer_opens_pdf():

    signer = PDFSigner(PDF_PATH)

    assert signer.document is not None

    signer.close()


def test_add_signature(tmp_path):

    output_path = (
        tmp_path /
        "signed.pdf"
    )

    signer = PDFSigner(PDF_PATH)

    signer.add_signature(
        signature_path=SIGNATURE_PATH,
        page_number=0,
        x=100,
        y=100,
        width=150,
        height=50
    )

    signer.save(output_path)
    signer.close()

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_invalid_page():

    signer = PDFSigner(PDF_PATH)

    with pytest.raises(IndexError):
        signer.add_signature(
            signature_path=SIGNATURE_PATH,
            page_number=999,
            x=100,
            y=100,
            width=150,
            height=50
        )

    signer.close()


def test_invalid_signature():

    missing_signature = (
        PROJECT_ROOT /
        "sample_files" /
        "missing.png"
    )

    signer = PDFSigner(PDF_PATH)

    with pytest.raises(FileNotFoundError):
        signer.add_signature(
            signature_path=missing_signature,
            page_number=0,
            x=100,
            y=100,
            width=150,
            height=50
        )

    signer.close()


def test_signature_outside_page():

    signer = PDFSigner(PDF_PATH)

    with pytest.raises(ValueError):
        signer.add_signature(
            signature_path=SIGNATURE_PATH,
            page_number=0,
            x=500,
            y=700,
            width=500,
            height=500
        )

    signer.close()


def test_cannot_overwrite_original():

    signer = PDFSigner(PDF_PATH)

    signer.add_signature(
        signature_path=SIGNATURE_PATH,
        page_number=0,
        x=100,
        y=100,
        width=150,
        height=50
    )

    with pytest.raises(ValueError):
        signer.save(PDF_PATH)

    signer.close()