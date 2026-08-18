import pytest

from backend.pdf_engine.coordinate_mapper import CoordinateMapper


@pytest.fixture
def mapper():
    return CoordinateMapper(
        pdf_width=612,
        pdf_height=792,
        display_width=816,
        display_height=1056
    )


def test_screen_to_pdf(mapper):

    pdf_x, pdf_y = mapper.screen_to_pdf(
        408,
        528
    )

    assert pdf_x == 306
    assert pdf_y == 396


def test_pdf_to_screen(mapper):

    screen_x, screen_y = mapper.pdf_to_screen(
        306,
        396
    )

    assert screen_x == 408
    assert screen_y == 528


def test_round_trip_conversion(mapper):

    original_x = 500
    original_y = 700

    pdf_x, pdf_y = mapper.screen_to_pdf(
        original_x,
        original_y
    )

    screen_x, screen_y = mapper.pdf_to_screen(
        pdf_x,
        pdf_y
    )

    assert screen_x == pytest.approx(original_x)
    assert screen_y == pytest.approx(original_y)


def test_rectangle_conversion(mapper):

    result = mapper.rectangle_screen_to_pdf(
        x=500,
        y=700,
        width=200,
        height=80
    )

    assert result["x"] == pytest.approx(375)
    assert result["y"] == pytest.approx(525)
    assert result["width"] == pytest.approx(150)
    assert result["height"] == pytest.approx(60)


def test_negative_coordinates_are_rejected(mapper):

    with pytest.raises(ValueError):
        mapper.screen_to_pdf(
            -10,
            100
        )


def test_invalid_rectangle_is_rejected(mapper):

    with pytest.raises(ValueError):
        mapper.rectangle_screen_to_pdf(
            x=800,
            y=700,
            width=200,
            height=80
        )