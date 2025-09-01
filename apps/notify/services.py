import requests
from django.conf import settings

ONE_SIGNAL_APP_ID = settings.ONESIGNAL_APP_ID
ONE_SIGNAL_API_KEY = settings.ONESIGNAL_API_KEY

def send_onesignal_notification(title, message, user=None):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONE_SIGNAL_API_KEY}",
    }

    payload = {
        "app_id": ONE_SIGNAL_APP_ID,
        "headings": {"en": title},
        "contents": {"en": message},
    }

    if user and hasattr(user, "player_id"): 
        payload["include_player_ids"] = [user.player_id]
    else:
        payload["included_segments"] = ["All"]

    response = requests.post("https://onesignal.com/api/v1/notifications", headers=headers, json=payload)
    return response.json()
