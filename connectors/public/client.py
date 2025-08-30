import requests
from django.conf import settings
import uuid
import base64
import hashlib
import hmac
import json
import time
from typing import List, Optional, Union


class WhiteBitClient:
    def get_markets(self):
        url = f"{settings.WHITEBIT_BASE_URL}/api/v4/public/markets"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"WhiteBIT API error: {str(e)}")


    def get_ticker(self):
        url = f"{settings.WHITEBIT_BASE_URL}/api/v4/public/ticker"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"WhiteBIT API error: {str(e)}")

        
    def get_fee(self):
        url = f"{settings.WHITEBIT_BASE_URL}/api/v4/public/fee"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"WhiteBIT API error: {str(e)}")


class WhiteBitPrivateClient():
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key
        
    def get_address(self, ticker, network=None):
        nonce = time.time_ns() // 1_000_000  
        
        url = f"{settings.WHITEBIT_BASE_URL}/api/v4/main-account/address"

        data = {
            "ticker": ticker,
            "request": "/api/v4/main-account/address",  
            "nonce": nonce
        }

        if network:
            data["network"] = network
        
        data_json = json.dumps(data, separators=(',', ':')) 
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



