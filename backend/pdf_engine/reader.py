import pymupdf
from pathlib import Path


class PDFReader:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                "The provided file is not a PDF."
            )

        try:
            self.document = pymupdf.open(self.pdf_path)
        except Exception as e:
            raise ValueError(
                f"Unable to open PDF: {e}"
            )

    def get_page_count(self) -> int:
        """Return the number of pages in the PDF."""
        return self.document.page_count

    def get_page_dimensions(self, page_number: int) -> dict:
        """Return the dimensions of a specific page."""

        if page_number < 0 or page_number >= self.document.page_count:
            raise IndexError(
                f"Page {page_number} does not exist."
            )

        page = self.document[page_number]
        rectangle = page.rect

        return {
            "width": rectangle.width,
            "height": rectangle.height
        }

    def get_page_info(self) -> list:
        """Return information about every page."""

        pages = []

        for page_number in range(self.document.page_count):
            page = self.document[page_number]
            rectangle = page.rect

            pages.append({
                "page": page_number + 1,
                "width": rectangle.width,
                "height": rectangle.height
            })

        return pages

    def close(self):
        """Close the PDF document."""
        self.document.close()