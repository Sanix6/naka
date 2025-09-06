import time
import json
import hmac
import hashlib
import base64
import requests

WHITEBIT_PUBLIC_KEY = "45f78aa66fb498abdae7c3883fb57ccd"
WHITEBIT_SECRET_KEY = "c27bb4c14b1e9eaff868548c1ff76d04"
WHITEBIT_BASE_URL = "https://whitebit.com"

class WhiteBitTradeClient:
    def __init__(self, public_key: str, secret_key: str):
        self.public_key = public_key
        self.secret_key = secret_key

    def transfer_to_main(self, ticker: str, amount: str):
        url = f"{WHITEBIT_BASE_URL}/api/v4/main-account/transfer"
        nonce = int(time.time() * 1000)

        data = {
            "ticker": ticker,
            "amount": amount,
            "from": "spot",   
            "to": "main",     
            "request": "/api/v4/main-account/transfer",
            "nonce": nonce,
        }

        data_json = json.dumps(data, separators=(',', ':'))
        payload = base64.b64encode(data_json.encode('ascii')).decode('ascii')

        signature = hmac.new(
            self.secret_key.encode('ascii'),
            payload.encode('ascii'),
            hashlib.sha512
        ).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "X-TXC-APIKEY": self.public_key,
            "X-TXC-PAYLOAD": payload,
            "X-TXC-SIGNATURE": signature,
        }

        try:
            response = requests.post(url, headers=headers, data=data_json)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Ошибка {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


if __name__ == "__main__":
    client = WhiteBitTradeClient(
        public_key=WHITEBIT_PUBLIC_KEY,
        secret_key=WHITEBIT_SECRET_KEY
    )

    result = client.transfer_to_main("LTC", "0.11252611")
    print(result)
