from pathlib import Path

from backend.pdf_engine.reader import PDFReader
from backend.pdf_engine.renderer import PDFRenderer
from backend.pdf_engine.signer import PDFSigner
from backend.pdf_engine.image_processor import SignatureImage
from backend.pdf_engine.coordinate_mapper import CoordinateMapper


class QuickSignService:

    def __init__(self, pdf_path: str):

        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

    def get_document_info(self) -> dict:
        """Return basic information about the PDF."""

        reader = PDFReader(self.pdf_path)

        try:
            page_count = reader.document.page_count

            pages = []

            for page_number in range(page_count):

                page = reader.document[page_number]

                pages.append({
                    "page_number": page_number,
                    "width": page.rect.width,
                    "height": page.rect.height
                })

            return {
                "filename": self.pdf_path.name,
                "page_count": page_count,
                "pages": pages
            }

        finally:
            reader.close()

    def render_page(
        self,
        page_number: int,
        output_path: str,
        scale: float = 2.0
    ):
        """Render one PDF page."""

        renderer = PDFRenderer(self.pdf_path)

        try:
            return renderer.render_page(
                page_number=page_number,
                output_path=output_path,
                scale=scale
            )

        finally:
            renderer.close()

    def sign_document(
        self,
        signature_path: str,
        page_number: int,
        x: float,
        y: float,
        width: float,
        height: float,
        output_path: str
    ):
        """Place a signature and save the signed PDF."""

        signer = PDFSigner(self.pdf_path)

        try:
            signer.add_signature(
                signature_path=signature_path,
                page_number=page_number,
                x=x,
                y=y,
                width=width,
                height=height
            )

            signer.save(output_path)

        finally:
            signer.close()

        return Path(output_path)
    
    def place_signature(
    self,
    signature_path: str,
    page_number: int,
    screen_x: float,
    screen_y: float,
    screen_width: float,
    screen_height: float,
    display_width: float,
    display_height: float,
    output_path: str
    ):
        """
        Convert frontend coordinates to PDF coordinates,
        place the signature, and save the PDF.
        """

        reader = PDFReader(self.pdf_path)

        try:
            page = reader.document[page_number]

            pdf_width = page.rect.width
            pdf_height = page.rect.height

        finally:
            reader.close()

        mapper = CoordinateMapper(
            pdf_width=pdf_width,
            pdf_height=pdf_height,
            display_width=display_width,
            display_height=display_height
        )

        signature = mapper.rectangle_screen_to_pdf(
            x=screen_x,
            y=screen_y,
            width=screen_width,
            height=screen_height
        )

        return self.sign_document(
            signature_path=signature_path,
            page_number=page_number,
            x=signature["x"],
            y=signature["y"],
            width=signature["width"],
            height=signature["height"],
            output_path=output_path
        )