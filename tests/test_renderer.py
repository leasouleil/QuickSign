from pathlib import Path

import pytest

from backend.pdf_engine.renderer import PDFRenderer


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = (
    PROJECT_ROOT /
    "sample_files" /
    "test.pdf"
)


def test_renderer_opens_pdf():

    renderer = PDFRenderer(PDF_PATH)

    assert renderer.document is not None

    renderer.close()


def test_page_dimensions():

    renderer = PDFRenderer(PDF_PATH)

    width, height = renderer.get_page_dimensions(
        page_number=0,
        scale=2.0
    )

    assert width > 0
    assert height > 0

    renderer.close()


def test_render_page(tmp_path):

    renderer = PDFRenderer(PDF_PATH)

    output_path = (
        tmp_path /
        "page.png"
    )

    renderer.render_page(
        page_number=0,
        output_path=output_path,
        scale=2.0
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0

    renderer.close()


def test_invalid_page():

    renderer = PDFRenderer(PDF_PATH)

    with pytest.raises(IndexError):
        renderer.render_page(
            page_number=999,
            output_path="invalid.png"
        )

    renderer.close()


def test_invalid_scale():

    renderer = PDFRenderer(PDF_PATH)

    with pytest.raises(ValueError):
        renderer.render_page(
            page_number=0,
            output_path="invalid.png",
            scale=0
        )

    renderer.close()