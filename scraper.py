import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_gold_data():
    try:
        # 1. جلب سعر الأونصة العالمي (من Binance)
        global_url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        global_res = requests.get(global_url, timeout=10)
        ounce_usd = float(global_res.json()['price'])
        gram_24_usd = ounce_usd / 31.1035

        # 2. جلب السعر المحلي عيار 21 (من موقع محلي كمثال)
        # ملاحظة: سنسحب من موقع "ايجبت جولد برايس" لأنه مستقر برمجياً
        local_url = "https://egypt.gold-price-today.com/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        local_res = requests.get(local_url, headers=headers, timeout=10)
        soup = BeautifulSoup(local_res.content, 'html.parser')
        
        # استخراج سعر عيار 21 (نبحث عن أول قيمة رقمية مرتبطة بعيار 21)
        price_21 = soup.find("td", text="عيار 21").find_next_sibling("td").text
        local_21_egp = float(price_21.replace("جنيه", "").replace(",", "").strip())

        # 3. العمليات الحسابية
        local_24_egp = local_21_egp * (24 / 21)
        sagha_dollar = local_24_egp / gram_24_usd

        # 4. تجهيز ملف البيانات
        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gold_21_egp": local_21_egp,
            "gold_24_usd": round(gram_24_usd, 2),
            "sagha_dollar": round(sagha_dollar, 2),
            "status": "success"
        }

        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("تم تحديث البيانات بنجاح!")

    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    get_gold_data()
