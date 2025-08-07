import requests
from django.conf import settings


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