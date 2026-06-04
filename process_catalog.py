import pdfplumber
import json
import base64
import re

# לוגו — המרה ל-base64
with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\img_Im0.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()
print(f"לוגו: {len(logo_b64)} תווים")

# חילוץ מוצרים מקטלוג 1
products1 = []
with pdfplumber.open(r"C:\Users\User\Downloads\קטלוג כללי 2026.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text(x_tolerance=3, y_tolerance=3)
        if not text:
            continue
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        # מחפש דפוס: מק"ט :XXX ואחריו מחיר
        j = 0
        while j < len(lines):
            line = lines[j]
            # מחפש מספרי קטלוג כמו 101, 102...
            m = re.search(r':מ"ק\s*(\d+)', line) or re.search(r'(\d{3})\s*:מ"ק', line)
            if not m:
                # ניסיון נוסף
                m = re.search(r'(\d{3})', line)
            if m and len(m.group(1)) == 3 and int(m.group(1)) >= 100:
                sku = m.group(1)
                # מחפש מחיר בשורה הבאה
                price_ils = 0
                price_usd = 0
                for k in range(j, min(j+4, len(lines))):
                    pm = re.search(r'(\d+)\s*\|\s*(\d+)', lines[k])
                    if pm:
                        price_usd = int(pm.group(1))
                        price_ils = int(pm.group(2))
                        break
                if price_ils > 0:
                    products1.append({
                        "sku": sku,
                        "name": f"סל פירות מק\"ט {sku}",
                        "price_ils": price_ils,
                        "price_usd": price_usd,
                        "catalog": "כללי 2026",
                        "page": i+1
                    })
            j += 1

# הסרת כפילויות
seen = set()
unique1 = []
for p in products1:
    if p['sku'] not in seen:
        seen.add(p['sku'])
        unique1.append(p)

# חילוץ מוצרים מקטלוג 2
products2 = []
with pdfplumber.open(r"C:\Users\User\Downloads\קטלוג שבועות תשפו.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text(x_tolerance=3, y_tolerance=3)
        if not text:
            continue
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        j = 0
        while j < len(lines):
            line = lines[j]
            m = re.search(r's(\d+)\s*:מ"ק', line) or re.search(r':מ"ק\s*s(\d+)', line)
            if not m:
                m = re.search(r'[sS](\d{3})', line)
            if m:
                sku = 's' + m.group(1)
                price_ils = 0
                price_usd = 0
                name_part = ""
                for k in range(j, min(j+5, len(lines))):
                    pm = re.search(r'(\d+)\s*\|\s*(\d+)', lines[k])
                    if pm:
                        price_usd = int(pm.group(1))
                        price_ils = int(pm.group(2))
                        # מחפש שם
                        after = lines[k][pm.end():].strip()
                        if len(after) > 2:
                            name_part = after
                        break
                if price_ils > 0:
                    name = f"עיצוב שבועות {sku}"
                    if name_part:
                        name = name_part + f" ({sku})"
                    products2.append({
                        "sku": sku,
                        "name": name,
                        "price_ils": price_ils,
                        "price_usd": price_usd,
                        "catalog": "שבועות תשפ\"ו",
                        "page": i+1
                    })
            j += 1

seen2 = set()
unique2 = []
for p in products2:
    if p['sku'] not in seen2:
        seen2.add(p['sku'])
        unique2.append(p)

all_products = unique1 + unique2

print(f"\nמוצרים קטלוג 1: {len(unique1)}")
for p in unique1[:5]:
    print(f"  {p['sku']}: ₪{p['price_ils']} / ${p['price_usd']}")

print(f"\nמוצרים קטלוג 2: {len(unique2)}")
for p in unique2[:5]:
    print(f"  {p['sku']}: {p['name']} — ₪{p['price_ils']} / ${p['price_usd']}")

# שמירה
output = {
    "logo_b64": logo_b64,
    "products": all_products
}
with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\catalog_data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nסה\"כ {len(all_products)} מוצרים נשמרו ב-catalog_data.json")
