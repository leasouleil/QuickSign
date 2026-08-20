from pathlib import Path

from backend.quicksignapp.service import QuickSignService


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


def test_get_document_info():

    service = QuickSignService(
        PDF_PATH
    )

    info = service.get_document_info()

    assert info["filename"] == "test.pdf"
    assert info["page_count"] > 0
    assert len(info["pages"]) == info["page_count"]


def test_render_page(tmp_path):

    service = QuickSignService(
        PDF_PATH
    )

    output_path = (
        tmp_path /
        "page.png"
    )

    result = service.render_page(
        page_number=0,
        output_path=output_path
    )

    assert result.exists()
    assert result.stat().st_size > 0


def test_sign_document(tmp_path):

    service = QuickSignService(
        PDF_PATH
    )

    output_path = (
        tmp_path /
        "signed.pdf"
    )

    result = service.sign_document(
        signature_path=SIGNATURE_PATH,
        page_number=0,
        x=100,
        y=100,
        width=150,
        height=50,
        output_path=output_path
    )

    assert result.exists()
    assert result.stat().st_size > 0