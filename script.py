import hashlib
import requests

def generate_hash(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# 🔹 Данные
BASE_URL = "https://skyfru.travelshop.aero/bitrix/components/travelshop/ibe.rest/"
TIMEOUT = 15
session_token = "0is5usmq03qhom4rp4jqju417e"
order_id = 1271

# 🔸 Генерация хэша: session_token + order_id (строкой)
raw_text = f"{session_token}{order_id}"
hash_value = generate_hash(raw_text)

# 🔸 Тело запроса
payload = {
    "session_token": session_token,
    "order_id": order_id,
    "hash": hash_value
}

# 🔹 Запрос
try:
    response = requests.post(
        url=f"{BASE_URL}CheckOrderPayment/",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=TIMEOUT
    )
    response.raise_for_status()
    data = response.json()

    if data.get("error") is None and data.get("error_code") == "OK":
        print("✅ Заказ оплачен.")
    else:
        print(f"❌ Не оплачен или ошибка: {data}")
except Exception as e:
    print(f"🚫 Ошибка запроса: {e}")
