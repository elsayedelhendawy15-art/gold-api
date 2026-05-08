import requests
import json
from datetime import datetime

def get_gold_data():
    try:
        # سحب سعر الذهب المباشر (Spot Gold) وهو الأدق لمحلات الصاغة
        # سنستخدم API يوفر بيانات البورصة العالمية لحظياً
        url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        response = requests.get(url, timeout=15)
        
        # السعر العالمي للأونصة
        price_float = float(response.json()['price'])
        
        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
            "gold_price_usd": price_float,
            "description": "Global Gold Spot Price (XAU/USD)",
            "status": "success"
        }

        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Success! Current Price: {price_float}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_gold_data()
