"""Format Naira amounts and spell them out in words (for cheques, invoices and receipts)."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

__all__ = ["to_words", "format_naira", "parse_naira", "kobo"]
__version__ = "0.1.0"

_ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
_SCALES = [(10**12, "trillion"), (10**9, "billion"), (10**6, "million"), (10**3, "thousand")]


def _to_decimal(amount: int | float | str | Decimal) -> Decimal:
    if isinstance(amount, str):
        amount = amount.replace("₦", "").replace("NGN", "").replace(",", "").strip()
    try:
        value = Decimal(str(amount))
    except InvalidOperation as exc:
        raise ValueError(f"Not a valid amount: {amount!r}") from exc
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _below_thousand(n: int) -> str:
    parts: list[str] = []
    hundreds, rest = divmod(n, 100)
    if hundreds:
        parts.append(f"{_ONES[hundreds]} hundred")
    if rest:
        if hundreds:
            parts.append("and")
        if rest < 20:
            parts.append(_ONES[rest])
        else:
            tens, ones = divmod(rest, 10)
            parts.append(_TENS[tens] + (f"-{_ONES[ones]}" if ones else ""))
    return " ".join(parts)


def _int_to_words(n: int) -> str:
    if n == 0:
        return "zero"
    parts: list[str] = []
    for value, name in _SCALES:
        if n >= value:
            count, n = divmod(n, value)
            parts.append(f"{_int_to_words(count)} {name}")
    if n:
        if parts and n < 100:
            parts.append("and")
        parts.append(_below_thousand(n))
    return " ".join(parts)


def to_words(amount: int | float | str | Decimal, *, title: bool = False, only: bool = True) -> str:
    """Spell out an amount, e.g. 1250.5 -> "one thousand, two hundred and fifty naira, fifty kobo only"."""
    value = _to_decimal(amount)
    if value < 0:
        return "minus " + to_words(-value, title=title, only=only)
    naira = int(value)
    k = int((value - naira) * 100)

    words = _int_to_words(naira)
    # comma between scale groups reads better on cheques
    for _, name in _SCALES:
        words = words.replace(f"{name} ", f"{name}, ").replace(f"{name}, and ", f"{name} and ")
    text = f"{words} naira"
    if k:
        text += f", {_int_to_words(k)} kobo"
    if only:
        text += " only"
    return text.title().replace(" And ", " and ") if title else text


def format_naira(amount: int | float | str | Decimal, *, symbol: str = "₦", decimals: bool = True) -> str:
    """1234567.8 -> "₦1,234,567.80"."""
    value = _to_decimal(amount)
    sign = "-" if value < 0 else ""
    body = f"{abs(value):,.2f}" if decimals else f"{abs(value):,.0f}"
    return f"{sign}{symbol}{body}"


def parse_naira(text: str) -> Decimal:
    """"₦1,234.50" -> Decimal("1234.50")."""
    return _to_decimal(text)


def kobo(amount: int | float | str | Decimal) -> int:
    """Convert naira to kobo (payment APIs like Paystack expect kobo): 1500.5 -> 150050."""
    return int(_to_decimal(amount) * 100)
