import requests
import time
import hashlib
import hmac
import json

import time
from typing import List, Optional, Union
from django.conf import settings
import base64
import uuid


class WhiteBitTradeClient:
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key
        
    def get_trade_history(self, market: str = None, limit: int = 50):
        url = "https://whitebit.com/api/v4/trade-account/executed-history"

        
        nonce = int(time.time() * 1000)

        data = {
            "market": "LTC_USDT",
            "limit": 100,
            "offset": 0,
            "request": "/api/v4/trade-account/executed-history",
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


    def create_transfer(self, ticker: str, amount: str, method: str):
        url = f"https://whitebit.com/api/v4/main-account/transfer"

        nonce = int(time.time() * 1000)

        data = {
            "ticker": ticker,
            "amount": amount,
            "method": method, 
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


    def transfer_to_main(self, ticker: str, amount: str):
        url = f"https://whitebit.com/api/v4/main-account/transfer"
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
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


    def withdraw(self, ticker: str, amount: str, address: str, network: str, uniqueId: str, memo: Optional[str] = None):
        url = f"https://whitebit.com/api/v4/main-account/withdraw"

        nonce = int(time.time() * 1000)

        data = {
            "ticker": ticker,
            "amount": amount,
            "address": address,
            "uniqueId": uniqueId, 
            "request": "/api/v4/main-account/withdraw",
            "nonce": nonce,
            "network": network,
        }

        if memo:
            data["memo"] = memo

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
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        
    





        




