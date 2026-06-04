import json
import re

with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\catalog_final.json", "r", encoding="utf-8") as f:
    data = json.load(f)

logo_b64 = data["logo"]
products = data["products"]

# בניית מערך מוצרים ל-JS
js_products = "[\n"
for p in products:
    name = p['name'].replace("'", "\\'").replace('"', '\\"')
    content = p['content'].replace("'", "\\'")
    catalog = p['catalog'].replace("'", "\\'").replace('"', '\\"')
    js_products += f'    {{ id: {p["id"]}, sku: "{p["sku"]}", name: "{name}", content: "{content}", length: 0, width: 0, weight: {p["weight"]}, price: {p["price"]}, price_usd: {p["price_usd"]}, catalog: "{catalog}" }},\n'
js_products += "  ]"

# קריאת HTML
with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# החלפת LOGO_SRC
old_logo = re.search(r"const LOGO_SRC = 'data:image/svg\+xml.*?';", html, re.DOTALL)
if old_logo:
    html = html[:old_logo.start()] + f"const LOGO_SRC = '{logo_b64}';" + html[old_logo.end():]
    print("לוגו הוחלף ✅")
else:
    print("לוגו לא נמצא ❌")

# החלפת מערך מוצרים
old_prods = re.search(r'products: \[[\s\S]*?\],\s*\n\s*nextId:', html)
if old_prods:
    html = html[:old_prods.start()] + f"products: {js_products},\n  nextId:" + html[old_prods.end()-len("  nextId:"):]
    print(f"מוצרים הוחלפו ({len(products)} מוצרים) ✅")
else:
    print("מוצרים לא נמצאו ❌")

# כתיבה חזרה
with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\index.html", "w", encoding="utf-8") as f:
    f.write(html)

# עדכון גם על שולחן העבודה
import shutil
shutil.copy(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\index.html",
            r"C:\Users\User\Desktop\izuv-bapri.html")

print("index.html עודכן ✅")
print(f"גודל קובץ: {len(html)/1024:.0f} KB")
