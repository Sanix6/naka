import hashlib
import requests


class APIClient:
    def ensure_valid_token(self):
        return "0v4cdt3bou00lpuc9e8degmgjm"


class PaymentService:
    BASE_URL = "https://skyfru.travelshop.aero/bitrix/components/travelshop/ibe.rest/"
    TIMEOUT = 60

    def __init__(self, api_client):
        self.api_client = api_client
        self.session = requests.Session()

    def generate_hash(self, *args) -> str:
        joined = ''.join(str(arg) for arg in args)
        hash_value = hashlib.md5(joined.encode('utf-8')).hexdigest()
        print(f"[DEBUG] Generated hash: {hash_value} from: {joined}")
        return hash_value

    def ticket(
        self,
        order_id: str = None,
        payment_id: str = None,
        rloc: str = None,
        additional_data: str = "",
        notify: str = "Y"
    ) -> dict:
        token = self.api_client.ensure_valid_token()

        ids = [bool(order_id), bool(payment_id), bool(rloc)]
        if ids.count(True) != 1:
            return {"error": "Specify only one of: order_id, payment_id, or rloc"}

        hash_input = [token]
        if order_id:
            hash_input.append(order_id)
        elif payment_id:
            hash_input.append(payment_id)
        else:
            hash_input.append(rloc)

        hash_input.extend([additional_data, notify])
        hash_str = self.generate_hash(*hash_input)

        data = {
            "session_token": token,
            "additional_data": additional_data,
            "notify": notify,
            "hash": hash_str
        }

        if order_id:
            data["order_id"] = order_id
        elif payment_id:
            data["payment_id"] = payment_id
        else:
            data["rloc"] = rloc

        try:
            response = self.session.post(
                url=f"{self.BASE_URL}Ticket/",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=self.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}


if __name__ == "__main__":
    api_client = APIClient()
    service = PaymentService(api_client)

    order_id = "1302"

    result = service.ticket(order_id=order_id)

    print("=== TICKET RESULT ===")
    if result.get("error"):
        print(f"❌ Ошибка: {result['error']}")
    else:
        print("✅ Успешный ответ:")
        for key, value in result.items():
            print(f"{key}: {value}")
