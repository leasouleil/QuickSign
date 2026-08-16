class CoordinateMapper:

    def __init__(
        self,
        pdf_width: float,
        pdf_height: float,
        display_width: float,
        display_height: float
    ):
        self.pdf_width = pdf_width
        self.pdf_height = pdf_height
        self.display_width = display_width
        self.display_height = display_height

        self._validate_dimensions()

    def _validate_dimensions(self):
        """Validate PDF and display dimensions."""

        dimensions = {
            "PDF width": self.pdf_width,
            "PDF height": self.pdf_height,
            "display width": self.display_width,
            "display height": self.display_height
        }

        for name, value in dimensions.items():
            if value <= 0:
                raise ValueError(
                    f"{name} must be greater than zero."
                )

    def validate_screen_rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float
    ):
        """Validate that a rectangle fits inside the displayed page."""

        if x < 0 or y < 0:
            raise ValueError(
                "Rectangle coordinates cannot be negative."
            )

        if width <= 0 or height <= 0:
            raise ValueError(
                "Rectangle dimensions must be greater than zero."
            )

        if x + width > self.display_width:
            raise ValueError(
                "Rectangle extends beyond the "
                "right edge of the displayed page."
            )

        if y + height > self.display_height:
            raise ValueError(
                "Rectangle extends beyond the "
                "bottom edge of the displayed page."
            )

    def screen_to_pdf(
        self,
        x: float,
        y: float
    ) -> tuple[float, float]:
        """Convert screen coordinates to PDF coordinates."""

        if x < 0 or y < 0:
            raise ValueError(
                "Screen coordinates cannot be negative."
            )

        pdf_x = (
            x *
            self.pdf_width /
            self.display_width
        )

        pdf_y = (
            y *
            self.pdf_height /
            self.display_height
        )

        return pdf_x, pdf_y

    def pdf_to_screen(
        self,
        x: float,
        y: float
    ) -> tuple[float, float]:
        """Convert PDF coordinates to screen coordinates."""

        if x < 0 or y < 0:
            raise ValueError(
                "PDF coordinates cannot be negative."
            )

        screen_x = (
            x *
            self.display_width /
            self.pdf_width
        )

        screen_y = (
            y *
            self.display_height /
            self.pdf_height
        )

        return screen_x, screen_y

    def rectangle_screen_to_pdf(
        self,
        x: float,
        y: float,
        width: float,
        height: float
    ) -> dict:
        """Convert a screen rectangle to PDF coordinates."""

        # Validate BEFORE converting.
        self.validate_screen_rectangle(
            x,
            y,
            width,
            height
        )

        pdf_x, pdf_y = self.screen_to_pdf(
            x,
            y
        )

        pdf_width = (
            width *
            self.pdf_width /
            self.display_width
        )

        pdf_height = (
            height *
            self.pdf_height /
            self.display_height
        )

        return {
            "x": pdf_x,
            "y": pdf_y,
            "width": pdf_width,
            "height": pdf_height
        }