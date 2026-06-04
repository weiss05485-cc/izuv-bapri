import re, shutil

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# החלפת ה-base64 הגדול בנתיב קובץ פשוט
html = re.sub(r"const LOGO_SRC = 'data:image/png;base64,[^']*';",
              "const LOGO_SRC = 'img_Im0.png';", html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

shutil.copy('index.html', r'C:\Users\User\Desktop\izuv-bapri.html')
print('Done, size:', len(html), 'bytes')
