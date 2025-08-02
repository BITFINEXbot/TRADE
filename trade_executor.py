import time
import hmac
import hashlib
import json
import requests
from config import API_KEY, API_SECRET

def execute_trade(symbol, side, usd_amount):
    url_path = "/v2/auth/w/order/submit"
    url = "https://api.bitfinex.com" + url_path

    nonce = str(int(time.time() * 1000000))
    def get_price(symbol):
    try:
        response = requests.get(f"https://api-pub.bitfinex.com/v2/ticker/{symbol}")
        data = response.json()
        return float(data[6])  # Last price
    except Exception as e:
        print(f"[❌] Грешка при взимане на цена: {e}")
        return None

# после в execute_trade
price = get_price(symbol)
if not price:
    return {"error": "Неуспешно извличане на текущата цена"}

qty = round(usd_amount / price, 6)
amount = str(qty if side == "BUY" else -qty)


    body = {
        "type": "MARKET",
        "symbol": symbol,
        "amount": amount
    }

    raw_body = json.dumps(body)
    signature_payload = f"/api{url_path}{nonce}{raw_body}".encode()
    signature = hmac.new(API_SECRET.encode(), signature_payload, hashlib.sha384).hexdigest()

    headers = {
        "bfx-nonce": nonce,
        "bfx-apikey": API_KEY,
        "bfx-signature": signature,
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=raw_body)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
