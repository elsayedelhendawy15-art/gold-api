import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_gold_data():
    try:
        # 1. جلب سعر الذهب العالمي (XAU/USD) - بديل دقيق لـ TradingView
        # سنستخدم مصدر يوفر بيانات TradingView بشكل مباشر وسريع
        global_url = "https://api.investing.com/api/financialdata/assets/pair/68?field=last_value" 
        headers = {'User-Agent': 'Mozilla/5.0'}
        global_res = requests.get(global_url, headers=headers, timeout=15)
        ounce_usd = float(global_res.json()['data'][0]['value'])
        gram_24_usd = ounce_usd / 31.1035

        # 2. جلب السعر المحلي المصري (عيار 21)
        local_url = "https://egypt.gold-price-today.com/"
        local_res = requests.get(local_url, headers=headers, timeout=15)
        soup = BeautifulSoup(local_res.content, 'html.parser')
        
        # البحث عن سعر عيار 21 في الجدول المحلي
        price_row = soup.find("td", string="عيار 21") or soup.find("td", text="عيار 21")
        local_21_egp = float(price_row.find_next_sibling("td").text.replace(",", "").strip())

        # 3. الحسابات
        local_24_egp = local_21_egp * (24 / 21)
        sagha_dollar = local_24_egp / gram_24_usd

        # 4. حفظ البيانات
        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "source": "TradingView-Style Data",
            "local": {
                "21k_egp": local_21_egp,
                "24k_egp": round(local_24_egp, 2)
            },
            "global": {
                "ounce_usd": round(ounce_usd, 2),
                "gram_24_usd": round(gram_24_usd, 2)
            },
            "metrics": {
                "sagha_dollar": round(sagha_dollar, 2)
            },
            "status": "success"
        }

        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"تم التحديث: السعر العالمي {ounce_usd}$ | دولار الصاغة {round(sagha_dollar, 2)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_gold_data()
