import pymupdf
from pathlib import Path


class PDFSigner:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError("The provided file is not a PDF.")

        try:
            self.document = pymupdf.open(self.pdf_path)
        except Exception as e:
            raise ValueError(f"Unable to open PDF: {e}")

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

        Coordinates use the PDF's coordinate system:
        - x: distance from the left
        - y: distance from the top
        """

        signature_path = Path(signature_path)

        if not signature_path.exists():
            raise FileNotFoundError(
                f"Signature file not found: {signature_path}"
            )

        if page_number < 0 or page_number >= self.document.page_count:
            raise IndexError(
                f"Page {page_number} does not exist."
            )

        if width <= 0 or height <= 0:
            raise ValueError(
                "Signature width and height must be greater than zero."
            )

        page = self.document[page_number]

        signature_rectangle = pymupdf.Rect(
            x,
            y,
            x + width,
            y + height
        )

        page.insert_image(
            signature_rectangle,
            filename=str(signature_path)
        )

    def save(self, output_path: str):
        """Save the signed PDF to a new file."""

        output_path = Path(output_path)

        self.document.save(output_path)

    def close(self):
        """Close the PDF document."""

        self.document.close()