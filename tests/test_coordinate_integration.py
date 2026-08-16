from pathlib import Path

from backend.pdf_engine.reader import PDFReader
from backend.pdf_engine.signer import PDFSigner
from backend.pdf_engine.coordinate_mapper import CoordinateMapper


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

OUTPUT_PATH = (
    PROJECT_ROOT /
    "sample_files" /
    "coordinate_test.pdf"
)


def main():

    # -----------------------------
    # 1. Read PDF dimensions
    # -----------------------------

    reader = PDFReader(PDF_PATH)

    page_info = reader.get_page_info()[0]

    pdf_width = page_info["width"]
    pdf_height = page_info["height"]

    reader.close()

    # -----------------------------
    # 2. Define displayed size
    # -----------------------------

    display_width = 816

    display_height = (
        pdf_height *
        display_width /
        pdf_width
    )

    # -----------------------------
    # 3. Create coordinate mapper
    # -----------------------------

    mapper = CoordinateMapper(
        pdf_width=pdf_width,
        pdf_height=pdf_height,
        display_width=display_width,
        display_height=display_height
    )

    # -----------------------------
    # 4. Simulate frontend
    # -----------------------------

    signature_screen = {
        "x": 500,
        "y": 700,
        "width": 200,
        "height": 80
    }

    # -----------------------------
    # 5. Convert screen → PDF
    # -----------------------------

    signature_pdf = (
        mapper.rectangle_screen_to_pdf(
            **signature_screen
        )
    )

    print("Screen coordinates:")
    print(signature_screen)

    print("\nPDF coordinates:")
    print(signature_pdf)

    # -----------------------------
    # 6. Sign PDF
    # -----------------------------

    signer = PDFSigner(PDF_PATH)

    signer.add_signature(
        signature_path=SIGNATURE_PATH,
        page_number=0,
        **signature_pdf
    )

    signer.save(OUTPUT_PATH)
    signer.close()

    print(
        f"\nCreated: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()