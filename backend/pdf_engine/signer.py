import pymupdf
from pathlib import Path


class PDFSigner:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

        self._validate_pdf()

        try:
            self.document = pymupdf.open(self.pdf_path)
        except Exception as e:
            raise ValueError(f"Unable to open PDF: {e}")

    def _validate_pdf(self):
        """Validate that the PDF exists and has the correct extension."""

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

        if not self.pdf_path.is_file():
            raise ValueError(
                f"The provided path is not a file: {self.pdf_path}"
            )

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                "The provided file is not a PDF."
            )

    def _validate_page(self, page_number: int):
        """Validate that the requested page exists."""

        if not isinstance(page_number, int):
            raise TypeError(
                "Page number must be an integer."
            )

        if page_number < 0 or page_number >= self.document.page_count:
            raise IndexError(
                f"Page {page_number} does not exist. "
                f"PDF contains {self.document.page_count} pages."
            )

    def _validate_signature(self, signature_path: Path):
        """Validate the signature image."""

        if not signature_path.exists():
            raise FileNotFoundError(
                f"Signature file not found: {signature_path}"
            )

        if not signature_path.is_file():
            raise ValueError(
                f"The signature path is not a file: {signature_path}"
            )

        supported_formats = {
            ".png",
            ".jpg",
            ".jpeg"
        }

        if signature_path.suffix.lower() not in supported_formats:
            raise ValueError(
                "Unsupported signature format. "
                "Use PNG, JPG, or JPEG."
            )

    def _validate_dimensions(
        self,
        width: float,
        height: float
    ):
        """Validate signature width and height."""

        if width <= 0:
            raise ValueError(
                "Signature width must be greater than zero."
            )

        if height <= 0:
            raise ValueError(
                "Signature height must be greater than zero."
            )

    def _validate_coordinates(
        self,
        page,
        x: float,
        y: float,
        width: float,
        height: float
    ):
        """
        Validate that the signature rectangle
        stays completely inside the PDF page.
        """

        if x < 0:
            raise ValueError(
                "Signature X coordinate cannot be negative."
            )

        if y < 0:
            raise ValueError(
                "Signature Y coordinate cannot be negative."
            )

        page_width = page.rect.width
        page_height = page.rect.height

        right = x + width
        bottom = y + height

        if right > page_width:
            raise ValueError(
                f"Signature extends beyond the right edge of the page. "
                f"Signature right edge: {right:.2f}, "
                f"page width: {page_width:.2f}."
            )

        if bottom > page_height:
            raise ValueError(
                f"Signature extends beyond the bottom edge of the page. "
                f"Signature bottom edge: {bottom:.2f}, "
                f"page height: {page_height:.2f}."
            )

    def add_signature(
        self,
        signature_path: str,
        page_number: int,
        x: float,
        y: float,
        width: float,
        height: float
    ):
        """
        Add a signature image to a PDF page.
        """

        signature_path = Path(signature_path)

        # 1. Validate page
        self._validate_page(page_number)

        # 2. Validate signature
        self._validate_signature(signature_path)

        # 3. Validate dimensions
        self._validate_dimensions(width, height)

        # 4. Get page
        page = self.document[page_number]

        # 5. Validate coordinates
        self._validate_coordinates(
            page,
            x,
            y,
            width,
            height
        )

        # 6. Create signature rectangle
        signature_rectangle = pymupdf.Rect(
            x,
            y,
            x + width,
            y + height
        )

        # 7. Insert signature
        page.insert_image(
            signature_rectangle,
            filename=str(signature_path)
        )

    def save(self, output_path: str):
        """Save the signed PDF to a new file."""

        output_path = Path(output_path)

        if output_path.resolve() == self.pdf_path.resolve():
            raise ValueError(
                "Output PDF cannot overwrite the original PDF."
        )

        self.document.save(output_path)

    def close(self):
        """Close the PDF document."""

        self.document.close()