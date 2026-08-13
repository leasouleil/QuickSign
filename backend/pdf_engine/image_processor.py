from pathlib import Path

from PIL import Image


class SignatureImage:
    SUPPORTED_FORMATS = {
        ".png",
        ".jpg",
        ".jpeg"
    }

    def __init__(self, image_path: str):
        self.image_path = Path(image_path)

        self._validate_file()

        try:
            self.image = Image.open(self.image_path)
            self.image.load()
        except Exception as e:
            raise ValueError(
                f"Unable to open signature image: {e}"
            )

        self._validate_image()

    def _validate_file(self):
        """Validate that the signature file exists and is supported."""

        if not self.image_path.exists():
            raise FileNotFoundError(
                f"Signature image not found: {self.image_path}"
            )

        if not self.image_path.is_file():
            raise ValueError(
                f"Signature path is not a file: {self.image_path}"
            )

        if self.image_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                "Unsupported signature format. "
                "Use PNG, JPG, or JPEG."
            )

    def _validate_image(self):
        """Validate that the image contains valid dimensions."""

        width, height = self.image.size

        if width <= 0 or height <= 0:
            raise ValueError(
                "Signature image has invalid dimensions."
            )

    def get_dimensions(self) -> tuple[int, int]:
        """Return the original image dimensions."""

        return self.image.size

    def get_aspect_ratio(self) -> float:
        """Return width / height."""

        width, height = self.image.size

        return width / height

    def resize_to_width(self, target_width: int) -> Image.Image:
        """
        Resize the signature to a specific width
        while preserving its aspect ratio.
        """

        if target_width <= 0:
            raise ValueError(
                "Target width must be greater than zero."
            )

        original_width, original_height = self.image.size

        aspect_ratio = original_height / original_width

        target_height = round(
            target_width * aspect_ratio
        )

        return self.image.resize(
            (target_width, target_height),
            Image.Resampling.LANCZOS
        )

    def resize_to_height(self, target_height: int) -> Image.Image:
        """
        Resize the signature to a specific height
        while preserving its aspect ratio.
        """

        if target_height <= 0:
            raise ValueError(
                "Target height must be greater than zero."
            )

        original_width, original_height = self.image.size

        aspect_ratio = original_width / original_height

        target_width = round(
            target_height * aspect_ratio
        )

        return self.image.resize(
            (target_width, target_height),
            Image.Resampling.LANCZOS
        )

    def convert_to_png(self, output_path: str):
        """Save the signature as PNG."""

        output_path = Path(output_path)

        image = self.image

        # PNG supports transparency.
        # Convert JPEG/RGB images to RGBA for consistency.
        if image.mode not in ("RGBA", "LA"):
            image = image.convert("RGBA")

        image.save(
            output_path,
            format="PNG"
        )

        return output_path

    def close(self):
        """Close the image."""

        self.image.close()