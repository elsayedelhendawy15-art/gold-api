import requests
import json
from datetime import datetime

def force_update():
    try:
        # سحب سعر الذهب المباشر
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=15)
        price_usd = float(res.json()['price'])
        
        # دي البيانات الجديدة اللي هتظهر في الملف
        new_data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "gold_price": round(price_usd, 2),
            "egypt_21k": round((price_usd / 31.1035) * 49.0 * 0.875, 0),
            "message": "SYSTEM_UPDATED_SUCCESSFULLY"
        }

        # حفظ في الملف
        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        print("Done!")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    force_update()
