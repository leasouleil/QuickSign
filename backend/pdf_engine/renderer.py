import pymupdf
from pathlib import Path


class PDFRenderer:

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

        self._validate_pdf()

        try:
            self.document = pymupdf.open(self.pdf_path)
        except Exception as e:
            raise ValueError(
                f"Unable to open PDF: {e}"
            )

    def _validate_pdf(self):
        """Validate the PDF path."""

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

        if not self.pdf_path.is_file():
            raise ValueError(
                f"Provided path is not a file: {self.pdf_path}"
            )

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                "The provided file is not a PDF."
            )

    def _validate_page(self, page_number: int):
        """Make sure the requested page exists."""

        if not isinstance(page_number, int):
            raise TypeError(
                "Page number must be an integer."
            )

        if page_number < 0 or page_number >= self.document.page_count:
            raise IndexError(
                f"Page {page_number} does not exist. "
                f"PDF contains {self.document.page_count} pages."
            )

    def render_page(
        self,
        page_number: int,
        output_path: str,
        scale: float = 2.0
    ):
        """
        Render a PDF page to a PNG image.

        scale:
            Controls the resolution of the rendered image.
            1.0 = normal PDF resolution
            2.0 = approximately double resolution
            3.0 = approximately triple resolution
        """

        self._validate_page(page_number)

        if scale <= 0:
            raise ValueError(
                "Scale must be greater than zero."
            )

        page = self.document[page_number]

        matrix = pymupdf.Matrix(
            scale,
            scale
        )

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        pixmap.save(output_path)

        return output_path

    def get_page_dimensions(
        self,
        page_number: int,
        scale: float = 1.0
    ) -> tuple[float, float]:
        """
        Return the rendered pixel dimensions
        of a PDF page.
        """

        self._validate_page(page_number)

        if scale <= 0:
            raise ValueError(
                "Scale must be greater than zero."
            )

        page = self.document[page_number]

        width = page.rect.width * scale
        height = page.rect.height * scale

        return width, height

    def close(self):
        """Close the PDF document."""

        self.document.close()