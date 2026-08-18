from pathlib import Path

import pytest
from PIL import Image

from backend.pdf_engine.image_processor import SignatureImage


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SIGNATURE_PATH = (
    PROJECT_ROOT /
    "sample_files" /
    "signaturetest.png"
)


def test_signature_exists():

    assert SIGNATURE_PATH.exists()


def test_signature_loads():

    signature = SignatureImage(
        SIGNATURE_PATH
    )

    width, height = signature.get_dimensions()

    assert width > 0
    assert height > 0

    signature.close()


def test_aspect_ratio():

    signature = SignatureImage(
        SIGNATURE_PATH
    )

    width, height = signature.get_dimensions()

    expected_ratio = width / height

    assert signature.get_aspect_ratio() == pytest.approx(
        expected_ratio
    )

    signature.close()


def test_resize_to_width():

    signature = SignatureImage(
        SIGNATURE_PATH
    )

    resized = signature.resize_to_width(300)

    assert resized.width == 300
    assert resized.height > 0

    signature.close()


def test_resize_to_height():

    signature = SignatureImage(
        SIGNATURE_PATH
    )

    resized = signature.resize_to_height(100)

    assert resized.height == 100
    assert resized.width > 0

    signature.close()


def test_invalid_width():

    signature = SignatureImage(
        SIGNATURE_PATH
    )

    with pytest.raises(ValueError):
        signature.resize_to_width(0)

    signature.close()


def test_invalid_height():

    signature = SignatureImage(
        SIGNATURE_PATH
    )

    with pytest.raises(ValueError):
        signature.resize_to_height(-10)

    signature.close()


def test_missing_signature():

    missing_path = (
        PROJECT_ROOT /
        "sample_files" /
        "does_not_exist.png"
    )

    with pytest.raises(FileNotFoundError):
        SignatureImage(missing_path)