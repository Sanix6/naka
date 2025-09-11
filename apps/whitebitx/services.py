from apps.whitebitx.models import Finance
import requests

def update_fees():
    url = "https://whitebit.com/api/v4/public/fee"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Ошибка при получении данных с Whitebit: {response.status_code}")
        return
    
    fees_data = response.json()

    for network_key, network_data in fees_data.items():
        currency_name = network_data.get("ticker")
        network_name = network_key

        withdrawal_fixed_fee = network_data.get("withdraw", {}).get("fixed")

        if currency_name and withdrawal_fixed_fee:
            if currency_name == network_name:
                try:
                    finance = Finance.objects.get(currency=currency_name, network="")
                    finance.fee = withdrawal_fixed_fee
                    finance.save()
                    print(f"Обновлен fee для {currency_name}")
                except Finance.DoesNotExist:
                    print(f"Запись для {currency_name} не найдена в базе, пропускаем.")
            else:
                full_network_name = f"{currency_name} ({network_name})"
                try:
                    finance = Finance.objects.get(currency=currency_name, network=full_network_name)
                    finance.fee = withdrawal_fixed_fee
                    finance.save()
                    print(f"Обновлен fee для {full_network_name}")
                except Finance.DoesNotExist:
                    print(f"Запись для {full_network_name} не найдена в базе, пропускаем.")
        else:
            print(f"Нет комиссии для вывода для {currency_name} - {network_name}")