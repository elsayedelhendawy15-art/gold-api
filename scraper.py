import requests
import json
from datetime import datetime

def get_live_data():
    try:
        # الرابط ده هو اللي بيجيب السعر الحقيقي
        url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        res = requests.get(url, timeout=15)
        price_usd = float(res.json()['price'])
        
        # حساب سعر عيار 21 (بافتراض دولار الصاغة 49 حالياً)
        # تقدر تغير الـ 49 دي لأي رقم انت عاوزه
        price_21k = (price_usd / 31.1035) * 49.0 * 0.875

        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "price": round(price_21k, 0),
            "global_usd": round(price_usd, 2)
        }

        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Success")
    except:
        print("Failed")

if __name__ == "__main__":
    get_live_data()
