import requests
import json
from datetime import datetime

def get_live_data():
    try:
        # 1. جلب سعر أونصة الذهب عالمياً من رابط Binance الفعلي
        # الرمز PAXG هو عملة مشفرة مدعومة بالذهب الحقيقي وتتحرك مع البورصة العالمية
        gold_url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        gold_res = requests.get(gold_url, timeout=15)
        price_oz_usd = float(gold_res.json()['price'])

        # 2. جلب سعر الدولار (استخدمنا رابطاً مستقراً وبسيطاً)
        usd_url = "https://api.exchangerate-api.com/v4/latest/USD" 
        usd_res = requests.get(usd_url, timeout=15)
        usd_rate = usd_res.json()['rates']['EGP'] 
        
        # إضافة "فرق الصاغة" كما فعلت أنت (منطق صحيح جداً)
        sagh_dollar_rate = usd_rate + 2.0 

        # 3. الحسابات البرمجية (معادلاتك صحيحة 100%)
        gram_24_usd = price_oz_usd / 31.1035
        price_24_egp = gram_24_usd * sagh_dollar_rate
        price_21_egp = price_24_egp * (21/24) # أو ضرب 0.875
        price_18_egp = price_24_egp * (18/24)

        # 4. تجهيز البيانات (JSON)
        data = {
            "metadata": {
                "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                "dollar_rate_used": sagh_dollar_rate
            },
            "prices": {
                "gold_24k": round(price_24_egp, 0), # التقريب لأقرب جنيه أفضل للعرض
                "gold_21k": round(price_21_egp, 0),
                "gold_18k": round(price_18_egp, 0),
                "gold_ounce_usd": round(price_oz_usd, 2)
            },
            "status": "success"
        }

        # حفظ الملف (تأكد من الاسم ليتطابق مع ملف الـ Actions)
        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"✅ Success: 21K Price is {data['prices']['gold_21k']}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_live_data()
