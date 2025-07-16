import hashlib
import requests


class APIClient:
    def ensure_valid_token(self):
        return "s4383kbp03b1mtoiqricvsuus7"


class PaymentStatusService:
    BASE_URL = "https://skyfru.travelshop.aero/bitrix/components/travelshop/ibe.rest/"
    TIMEOUT = 60

    def __init__(self, api_client):
        self.api_client = api_client
        self.session = requests.Session()

    def generate_hash(self, *args) -> str:
        # Хеширует значения с помощью MD5
        joined = ''.join(str(arg) for arg in args)
        hash_value = hashlib.md5(joined.encode("utf-8")).hexdigest()
        print(f"[DEBUG] Hash: {hash_value} from: {joined}")
        return hash_value

    def check_order_payment(self, order_id: int) -> dict:
        token = self.api_client.ensure_valid_token()
        hash_value = self.generate_hash(token, order_id)

        payload = {
            "session_token": token,
            "order_id": order_id,
            "hash": hash_value
        }

        try:
            response = self.session.post(
                url=f"{self.BASE_URL}CheckOrderPayment/",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}


if __name__ == "__main__":
    api_client = APIClient()
    service = PaymentStatusService(api_client)

    order_id = 1293  

    result = service.check_order_payment(order_id=order_id)

    print("=== CHECK ORDER PAYMENT RESULT ===")
    if result.get("error"):
        print(f"❌ Ошибка: {result['error']}")
    else:
        print("✅ Ответ сервера:")
        for key, value in result.items():
            print(f"{key}: {value}")
