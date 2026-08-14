from pathlib import Path

from backend.pdf_engine.renderer import PDFRenderer


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = (
    PROJECT_ROOT /
    "sample_files" /
    "test.pdf"
)

OUTPUT_DIR = (
    PROJECT_ROOT /
    "sample_files" /
    "rendered"
)


def main():

    renderer = PDFRenderer(PDF_PATH)

    print(
        f"PDF contains "
        f"{renderer.document.page_count} pages."
    )

    for page_number in range(
        renderer.document.page_count
    ):

        output_path = (
            OUTPUT_DIR /
            f"page_{page_number + 1}.png"
        )

        renderer.render_page(
            page_number=page_number,
            output_path=output_path,
            scale=2.0
        )

        width, height = renderer.get_page_dimensions(
            page_number=page_number,
            scale=2.0
        )

        print(
            f"Page {page_number + 1}: "
            f"{width:.0f} × {height:.0f}px"
        )

        print(
            f"Saved: {output_path}"
        )

    renderer.close()


if __name__ == "__main__":
    main()