from pathlib import Path

from backend.pdf_engine.signer import PDFSigner


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = PROJECT_ROOT / "sample_files" / "test.pdf"
SIGNATURE_PATH = PROJECT_ROOT / "sample_files" / "signaturetest.png"
OUTPUT_PATH = PROJECT_ROOT / "sample_files" / "signed_test.pdf"


def main():

    signer = PDFSigner(PDF_PATH)

    signer.add_signature(
        signature_path=SIGNATURE_PATH,
        page_number=0,
        x=400,
        y=650,
        width=150,
        height=50
    )

    signer.save(OUTPUT_PATH)
    signer.close()

    print(f"Signed PDF created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()