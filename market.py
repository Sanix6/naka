import time
import json
import base64
import hmac
import hashlib
import requests
from requests.exceptions import RequestException
from django.conf import settings

WHITEBIT_BASE_URL = "https://whitebit.com"

class WhiteBitPrivateClient:
    def __init__(self, public_key: str, secret_key: str):
        self.public_key = public_key
        self.secret_key = secret_key

    def create_market_order(self, market: str, side: str, amount: float):
        url = f"https://whitebit.com/api/v4/order/stock_market"
        
        nonce = int(time.time() * 1000)
        
        data = {
            "market": market,
            "side": side,
            "amount": amount,
            "request": "/api/v4/order/stock_market",
            "nonce": nonce
        }

        data_json = json.dumps(data, separators=(',', ':'))

        payload = base64.b64encode(data_json.encode('ascii')).decode('ascii')

        signature = hmac.new(
            self.secret_key.encode('ascii'),
            payload.encode('ascii'),
            hashlib.sha512
        ).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            'X-TXC-APIKEY': self.public_key,
            'X-TXC-PAYLOAD': payload,
            'X-TXC-SIGNATURE': signature,
        }

        try:
            response = requests.post(url, headers=headers, data=data_json)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Ошибка {response.status_code}: {response.text}"}
        except RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

if __name__ == "__main__":
    public_key = "45f78aa66fb498abdae7c3883fb57ccd"
    secret_key = "c27bb4c14b1e9eaff868548c1ff76d04"
    client = WhiteBitPrivateClient(public_key, secret_key)

    market = "LTC_USDT"  
    side = "sell"  
    amount = 0.11000

    result = client.create_market_order(market, side, amount)
    print(result)
