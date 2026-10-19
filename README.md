# naira-words

Format Naira amounts and spell them out in words — for cheques, invoices, receipts and payment pages. Pure Python, no dependencies, uses `Decimal` so there are no floating-point surprises.

```bash
pip install git+https://github.com/xacking/naira-words
```

```python
from naira_words import to_words, format_naira, parse_naira, kobo

to_words(1250.50)
# 'one thousand, two hundred and fifty naira, fifty kobo only'

to_words(2_500_000, title=True)
# 'Two Million, Five Hundred Thousand Naira Only'

format_naira(1234567.8)      # '₦1,234,567.80'
format_naira(50, symbol="NGN ")  # 'NGN 50.00'
parse_naira("₦1,234.50")     # Decimal('1234.50')
kobo(1500.50)                # 150050  (Paystack / Flutterwave expect kobo)
```

Accepts `int`, `float`, `Decimal` or strings like `"₦1,000.00"` / `"NGN 1000"`. Amounts are rounded half-up to the nearest kobo.

## License

MIT
