import json
import re
import base64
import pdfplumber

# קריאת לוגו
with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\img_Im0.png", "rb") as f:
    logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode()

# חילוץ מוצרים נקי — רק מק"ט ומחיר
products = []
pid = 1

# קטלוג 1 — מק"טים 101-250
with pdfplumber.open(r"C:\Users\User\Downloads\קטלוג כללי 2026.pdf") as pdf:
    seen = set()
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        # מחפש זוגות: מספר 3 ספרות | מחיר
        pairs = re.findall(r'(\d{3})\s*:.*?(\d{2,3})\s*\|\s*(\d{3,4})', text)
        for sku, usd, ils in pairs:
            sku_num = int(sku)
            if 100 <= sku_num <= 250 and sku not in seen:
                seen.add(sku)
                products.append({
                    "id": pid, "sku": sku,
                    "name": f"סל פירות מק\"ט {sku}",
                    "content": "פירות עונתיים בעיצוב מיוחד",
                    "length": 0, "width": 0, "weight": 0,
                    "price": int(ils),
                    "price_usd": int(usd),
                    "catalog": "כללי 2026"
                })
                pid += 1

print(f"קטלוג 1: {len(products)} מוצרים")

# קטלוג 2 — שבועות, מק"טים s101-s120
count_before = len(products)
with pdfplumber.open(r"C:\Users\User\Downloads\קטלוג שבועות תשפו.pdf") as pdf:
    seen2 = set()
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        # s101, s102 וכו'
        pairs = re.findall(r'[sS](\d{3})\s*:.*?(\d{1,3})\s*\|\s*(\d{2,4})', text)
        for sku_n, usd, ils in pairs:
            sku = 's' + sku_n
            if sku not in seen2:
                seen2.add(sku)
                products.append({
                    "id": pid, "sku": sku,
                    "name": f"עיצוב שבועות מק\"ט {sku}",
                    "content": "עיצוב מיוחד לשבועות",
                    "length": 0, "width": 0, "weight": 0,
                    "price": int(ils),
                    "price_usd": int(usd),
                    "catalog": "שבועות תשפ\"ו"
                })
                pid += 1

print(f"קטלוג 2: {len(products) - count_before} מוצרים")
print(f"סה\"כ: {len(products)} מוצרים")

# שמירה לקובץ JS
js_products = json.dumps(products, ensure_ascii=False, indent=2)

output = {
    "logo": logo_b64,
    "products_js": js_products,
    "products": products
}

with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\catalog_final.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("נשמר catalog_final.json")

# הדפסת דוגמאות
print("\n5 מוצרים ראשונים מקטלוג 1:")
for p in products[:5]:
    print(f"  {p['sku']}: ₪{p['price']} (${p['price_usd']})")

print("\n5 מוצרים ראשונים מקטלוג 2:")
for p in [x for x in products if x['catalog'] != 'כללי 2026'][:5]:
    print(f"  {p['sku']}: ₪{p['price']} (${p['price_usd']})")
