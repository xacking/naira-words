from decimal import Decimal

import pytest

from naira_words import format_naira, kobo, parse_naira, to_words


@pytest.mark.parametrize(
    "amount,expected",
    [
        (0, "zero naira only"),
        (5, "five naira only"),
        (21, "twenty-one naira only"),
        (100, "one hundred naira only"),
        (1005, "one thousand and five naira only"),
        (1250.5, "one thousand, two hundred and fifty naira, fifty kobo only"),
        (2_500_000, "two million, five hundred thousand naira only"),
        ("₦1,000,000.01", "one million naira, one kobo only"),
    ],
)
def test_to_words(amount, expected):
    assert to_words(amount) == expected


def test_title_and_only():
    assert to_words(15, title=True, only=False) == "Fifteen Naira"
    assert to_words(-3) == "minus three naira only"


def test_format_and_parse():
    assert format_naira(1234567.8) == "₦1,234,567.80"
    assert format_naira(-50, decimals=False) == "-₦50"
    assert format_naira(10, symbol="NGN ") == "NGN 10.00"
    assert parse_naira("₦1,234.50") == Decimal("1234.50")


def test_kobo():
    assert kobo(1500.5) == 150050
    assert kobo("0.1") == 10


def test_invalid():
    with pytest.raises(ValueError):
        to_words("abc")
