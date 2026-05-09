import requests
import json
from datetime import datetime

def get_gold():
    try:
        # سحب السعر العالمي
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=15)
        price_usd = float(res.json()['price'])
        
        # حساب السعر (عيار 21)
        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M %p"),
            "price_21k": round((price_usd / 31.1035) * 49.0 * 0.875, 0),
            "global_usd": price_usd,
            "status": "SUCCESS_FORCE_UPDATE"
        }

        # السطر ده هو اللي هيكريت الملف لو مش موجود
        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("File Created Successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_gold()
