import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. בדיקת LOGO_SRC
m = re.search(r'const LOGO_SRC = (.{0,60})', content)
print('LOGO:', m.group(1) if m else 'NOT FOUND')

# 2. בדיקת products
prod_start = content.find('products: [')
prod_end = content.find('],\n  nextId:', prod_start)
print('products start:', prod_start, 'end:', prod_end)

# 3. גודל
print('Size:', len(content), 'bytes')

# 4. בדיקת syntax - מחפש backslash לפני אות עברית
bad_backslash = []
for i, ch in enumerate(content[prod_start:prod_end]):
    if ch == '\\' and i+1 < prod_end-prod_start:
        next_ch = content[prod_start+i+1]
        if ord(next_ch) > 127:
            bad_backslash.append((i, next_ch, content[prod_start+max(0,i-10):prod_start+i+15]))
if bad_backslash:
    print('BAD BACKSLASH FOUND:')
    for pos, ch, ctx in bad_backslash[:5]:
        print(f'  pos {pos}: before "{ch}" - context: {repr(ctx)}')
else:
    print('No bad backslashes')

# 5. בדיקת quotes לא סגורות
# ספירת מרכאות כפולות
q_count = content[prod_start:prod_end].count('"')
print(f'Double quotes in products: {q_count} ({"odd - PROBLEM!" if q_count % 2 else "even - OK"})')
