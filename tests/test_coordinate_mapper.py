from backend.pdf_engine.coordinate_mapper import CoordinateMapper


def main():

    mapper = CoordinateMapper(
        pdf_width=612,
        pdf_height=792,
        display_width=816,
        display_height=1056
    )

    # -----------------------------
    # Screen → PDF
    # -----------------------------

    screen_x = 408
    screen_y = 528

    pdf_x, pdf_y = mapper.screen_to_pdf(
        screen_x,
        screen_y
    )

    print("Screen coordinates:")
    print(f"X: {screen_x}")
    print(f"Y: {screen_y}")

    print("\nPDF coordinates:")
    print(f"X: {pdf_x}")
    print(f"Y: {pdf_y}")

    # -----------------------------
    # PDF → Screen
    # -----------------------------

    converted_x, converted_y = (
        mapper.pdf_to_screen(
            pdf_x,
            pdf_y
        )
    )

    print("\nConverted back to screen:")
    print(f"X: {converted_x}")
    print(f"Y: {converted_y}")

    # -----------------------------
    # Rectangle conversion
    # -----------------------------

    signature = mapper.rectangle_screen_to_pdf(
        x=500,
        y=700,
        width=200,
        height=80
    )

    print("\nSignature rectangle:")
    print(signature)


if __name__ == "__main__":
    main()