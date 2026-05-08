import requests
import json
from datetime import datetime

def get_gold_data():
    try:
        # جلب السعر العالمي فقط للتجربة والتأكد من نجاح الـ API
        global_url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        global_res = requests.get(global_url, timeout=10)
        ounce_usd = float(global_res.json()['price'])
        
        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ounce_usd": ounce_usd,
            "status": "online"
        }

        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("Success: File Created!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_gold_data()
