from decimal import Decimal, ROUND_DOWN

# Пример входных данных
currency_from = {'decimal': 2}  # Например, для валюты с 2 знаками после запятой
currency_to = {'decimal': 3}  # Для другой валюты с 3 знаками после запятой

# Количество знаков после запятой
decimal_places_from = currency_from.get('decimal', 8)
decimal_places_to = currency_to.get('decimal', 8)

# Пример значений для amount_from и amount_to
amount_from = Decimal(123.456789)  # Пример значения, которое надо округлить
amount_to = Decimal(987.654321)

# Округление с учетом decimal_places
if amount_from:
    amount_from = amount_from.quantize(Decimal(10) ** -decimal_places_from, rounding=ROUND_DOWN)

if amount_to:
    amount_to = amount_to.quantize(Decimal(10) ** -decimal_places_to, rounding=ROUND_DOWN)

# Выводим результат
print(f"Округленное значение amount_from: {amount_from}")
print(f"Округленное значение amount_to: {amount_to}")
