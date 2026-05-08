import requests
import json
from datetime import datetime

def get_gold_data():
    try:
        # سحب السعر العالمي للذهب (XAU/USD) 
        # هذا الرابط يوفر بيانات حية دقيقة جداً
        url = "https://api.investing.com/api/financialdata/assets/pair/68?field=last_value"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        
        # استخراج السعر من النتيجة
        gold_price_usd = float(response.json()['data'][0]['value'])
        
        # تجهيز البيانات النهائية
        data = {
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "gold_price_usd": gold_price_usd,
            "unit": "Ounce",
            "status": "success"
        }

        # حفظ الملف ليكون متاحاً كـ API
        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Done! Current Gold Price: {gold_price_usd}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_gold_data()
