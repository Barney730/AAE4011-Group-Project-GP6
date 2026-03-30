# utils/alert.py
import requests
import time

def send_telegram_alert(message: str, bot_token: str, chat_id: str):
    """Send loud alert via Telegram (forces notification sound on most devices)"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"🚨 GUARDIAN AI ALERT 🚨\n{message}",
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            print(f"✅ Telegram alert sent: {message}")
        else:
            print(f"⚠️ Telegram failed: {response.text}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def send_blynk_alert(value: int, auth_token: str, pin: int = 1):
    """Simple Blynk virtual pin update (legacy)"""
    try:
        url = f"http://blynk.cloud/external/api/update?token={auth_token}&V{pin}={value}"
        requests.get(url, timeout=3)
        print(f"✅ Blynk visual alert sent (V{pin} = {value})")
    except Exception as e:
        print(f"⚠️ Blynk error: {e}")
