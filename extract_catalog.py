import pdfplumber
import json
import base64
from pypdf import PdfReader
import io

def extract_pdf(path, name):
    print(f"\n=== {name} ===")
    results = []
    with pdfplumber.open(path) as pdf:
        print(f"סה\"כ עמודים: {len(pdf.pages)}")
        for i, page in enumerate(pdf.pages[:30]):  # ראשון 30 עמודים
            text = page.extract_text()
            if text and text.strip():
                results.append({"page": i+1, "text": text.strip()})
    return results

# חילוץ טקסט
catalog1 = extract_pdf(r"C:\Users\User\Downloads\קטלוג כללי 2026.pdf", "קטלוג כללי 2026")
catalog2 = extract_pdf(r"C:\Users\User\Downloads\קטלוג שבועות תשפו.pdf", "קטלוג שבועות תשפו")

# שמירה לקובץ
with open(r"C:\Users\User\Desktop\תיקיית קלוד\izuv-bapri\catalog_text.json", "w", encoding="utf-8") as f:
    json.dump({"catalog1": catalog1, "catalog2": catalog2}, f, ensure_ascii=False, indent=2)

print("\n=== תוצאות קטלוג 1 ===")
for p in catalog1[:10]:
    print(f"\n--- עמוד {p['page']} ---")
    print(p['text'][:500])

print("\n=== תוצאות קטלוג 2 ===")
for p in catalog2[:10]:
    print(f"\n--- עמוד {p['page']} ---")
    print(p['text'][:500])

# חילוץ תמונות מהעמוד הראשון (לוגו)
print("\n=== מחלץ תמונות מעמוד 1 ===")
reader = PdfReader(r"C:\Users\User\Downloads\קטלוג כללי 2026.pdf")
page = reader.pages[0]
if '/Resources' in page and '/XObject' in page['/Resources']:
    xobjects = page['/Resources']['/XObject']
    for name, obj in xobjects.items():
        o = obj.get_object()
        if o.get('/Subtype') == '/Image':
            data = o.get_data()
            w = o.get('/Width', 0)
            h = o.get('/Height', 0)
            cs = o.get('/ColorSpace', '')
            print(f"  תמונה: {name}, {w}x{h}, ColorSpace: {cs}")
            if w and h:
                ext = 'jpg' if o.get('/Filter') == '/DCTDecode' else 'png'
                fname = f"C:\\Users\\User\\Desktop\\תיקיית קלוד\\izuv-bapri\\img_{name[1:]}.{ext}"
                with open(fname, 'wb') as f:
                    f.write(data)
                print(f"  נשמר: {fname}")
