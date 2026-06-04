import json
import re
import base64
import pdfplumber

# לוגו
with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\img_Im0.png", "rb") as f:
    logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode()

products = []
pid = 1

# קטלוג 1
seen = set()
with pdfplumber.open(r"C:\Users\User\Downloads\קטלוג כללי 2026.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        # חיפוש כל מספרי 3 ספרות עם תבנית מחיר: XX | XXX
        # פורמט: [מספר 3 ספרות] ...newline... [XX | XXX] (דולר | שקל)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            # מחפש שורה עם מחיר בתבנית מספר|מספר
            m = re.search(r'\b(\d{2,3})\s*\|\s*(\d{3,4})\b', line)
            if m:
                usd = int(m.group(1))
                ils = int(m.group(2))
                # מחפש מק"ט בשורות קרובות
                for j in range(max(0,i-3), i+1):
                    # מחפש מספר 3 ספרות שנראה כמו מק"ט (100-250)
                    nums = re.findall(r'\b(1\d{2}|2[0-4]\d|250)\b', lines[j])
                    for sku in nums:
                        if sku not in seen and 100 <= int(sku) <= 250 and ils >= 200:
                            seen.add(sku)
                            products.append({
                                "id": pid, "sku": sku,
                                "name": f'סל פירות מק"ט {sku}',
                                "content": "פירות עונתיים בעיצוב מיוחד",
                                "length": 0, "width": 0, "weight": 0,
                                "price": ils,
                                "price_usd": usd,
                                "catalog": "כללי 2026"
                            })
                            pid += 1

print(f"קטלוג 1: {len(products)} מוצרים")

# קטלוג 2 — שבועות
count_before = len(products)
seen2 = set()
with pdfplumber.open(r"C:\Users\User\Downloads\קטלוג שבועות תשפו.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        lines = text.split('\n')
        for i, line in enumerate(lines):
            m = re.search(r'\b(\d{1,3})\s*\|\s*(\d{2,4})\b', line)
            if m:
                usd = int(m.group(1))
                ils = int(m.group(2))
                for j in range(max(0,i-3), i+1):
                    # מק"טים של שבועות: s101-s130
                    snums = re.findall(r'\b(1\d{2})\b', lines[j])
                    for sn in snums:
                        sku = 's' + sn
                        if sku not in seen2 and ils >= 30:
                            seen2.add(sku)
                            products.append({
                                "id": pid, "sku": sku,
                                "name": f'עיצוב שבועות מק"ט {sku}',
                                "content": "עיצוב מיוחד לשבועות",
                                "length": 0, "width": 0, "weight": 0,
                                "price": ils,
                                "price_usd": usd,
                                "catalog": 'שבועות תשפ"ו'
                            })
                            pid += 1

print(f"קטלוג 2: {len(products)-count_before} מוצרים")
print(f"סה\"כ: {len(products)} מוצרים")

for p in products[:5]:
    print(f"  {p['sku']}: ₪{p['price']} / ${p['price_usd']}")

with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\catalog_final.json", "w", encoding="utf-8") as f:
    json.dump({"logo": logo_b64, "products": products}, f, ensure_ascii=False, indent=2)
print("נשמר!")
