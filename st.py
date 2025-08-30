import json
import time
import base64
import hmac
import hashlib
import requests

class WhiteBitPrivateClient:
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key

    def get_history(self, transactionMethod, ticker=None, address=None, memo=None, 
                    addresses=None, uniqueId=None, limit=50, offset=0, status=None):
        nonce = time.time_ns() // 1_000_000  
        
        url = f"https://whitebit.com/api/v4/main-account/history"

        params = {
            "transactionMethod": transactionMethod,
            "ticker": ticker,
            "address": address,
            "memo": memo,
            "addresses": addresses,
            "uniqueId": uniqueId,
            "limit": limit,
            "offset": offset,
            "status": status,
            "nonce": nonce,
            "request": "/api/v4/main-account/history"
        }

        data_json = json.dumps(params, separators=(',', ':'))  
        
        payload = base64.b64encode(data_json.encode('ascii')).decode('ascii')

        signature = hmac.new(self.secret_key.encode('ascii'), payload.encode('ascii'), hashlib.sha512).hexdigest()

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
        
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

# Пример использования
if __name__ == "__main__":
    public_key = "45f78aa66fb498abdae7c3883fb57ccd" 
    secret_key = "c27bb4c14b1e9eaff868548c1ff76d04"  # Замените на строку

    client = WhiteBitPrivateClient(public_key, secret_key)
    
    response = client.get_history(
        transactionMethod=1,
        ticker="BTC",
        address="1FfobFgksuHh64Fq1zPhtTQZQgxh97Bpmm",
        memo="Test memo",
        addresses=["address1", "address2"],
        uniqueId="unique-id-12345",
        limit=100,
        offset=0,
        status=[3, 7]
    )
    
    print(json.dumps(response, indent=4))
