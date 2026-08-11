from pathlib import Path

from backend.pdf_engine.reader import PDFReader


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "sample_files" / "test.pdf"


def main():
    reader = PDFReader(PDF_PATH)

    print(f"PDF: {PDF_PATH}")
    print(f"Pages: {reader.get_page_count()}")

    print("\nPage information:")

    for page in reader.get_page_info():
        print(
            f"Page {page['page']}: "
            f"{page['width']:.2f} x {page['height']:.2f}"
        )

    reader.close()


if __name__ == "__main__":
    main()