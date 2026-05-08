import requests
import json
from datetime import datetime

def get_live_data():
    try:
        # 1. جلب سعر أونصة الذهب عالمياً من رابط Binance الفعلي (PAXG/USDT)
        gold_url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        gold_res = requests.get(gold_url, timeout=15)
        price_oz_usd = float(gold_res.json()['price'])

        # 2. جلب سعر الدولار الرسمي (كمصدر مستقر)
        usd_url = "https://api.exchangerate-api.com/v4/latest/USD" 
        usd_res = requests.get(usd_url, timeout=15)
        usd_rate = usd_res.json()['rates']['EGP'] 
        
        # 3. دولار الصاغة (نزيد 2 جنيه عن الرسمي أو حسب ما تريد)
        sagh_dollar_rate = usd_rate + 2.0 

        # 4. الحسابات (الأونصة -> جرام 24 -> جرام 21)
        gram_24_usd = price_oz_usd / 31.1035
        price_24_egp = gram_24_usd * sagh_dollar_rate
        price_21_egp = price_24_egp * 0.875

        # 5. البيانات النهائية
        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "price": round(price_21_egp, 0), # هذا سيغير الـ 3600
            "global_ounce": round(price_oz_usd, 2),
            "dollar_used": sagh_dollar_rate,
            "status": "success"
        }

        # حفظ الملف (تأكد من الاسم gold_data.json)
        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Update Success: 21K = {data['price']}")

    except Exception as e:
        print(f"Update Failed: {e}")

if __name__ == "__main__":
    get_live_data()
