import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()
import requests
from apps.whitebitx.models import Finance

url = "https://whitebit.com/api/v4/public/markets"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    for market in data:
        stock = market.get("stock")
        stock_prec = market.get("stockPrec")

        if stock and stock_prec is not None:
            try:
                finances = Finance.objects.filter(currency=stock)
                
                for finance in finances:
                    finance.decimal = int(stock_prec)
                    finance.save()

                print(f"Updated {stock} decimal to {stock_prec} for {finances.count()} entries.")
            except Finance.DoesNotExist:
                print(f"Currency {stock} not found in Finance model.")
else:
    print("Error fetching data from Whitebit API:", response.status_code)
