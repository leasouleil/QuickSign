from pathlib import Path

from backend.pdf_engine.image_processor import SignatureImage


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SIGNATURE_PATH = (
    PROJECT_ROOT /
    "sample_files" /
    "signaturetest.png"
)


def main():

    signature = SignatureImage(SIGNATURE_PATH)

    original_width, original_height = (
        signature.get_dimensions()
    )

    print("Original:")
    print(
        f"{original_width} × {original_height}"
    )

    resized = signature.resize_to_width(300)

    resized_width, resized_height = resized.size

    print("\nResized:")
    print(
        f"{resized_width} × {resized_height}"
    )

    signature.close()


if __name__ == "__main__":
    main()