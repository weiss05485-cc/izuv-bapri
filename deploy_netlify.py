import urllib.request
import json

# קרא את קובץ ה-ZIP
with open('deploy.zip', 'rb') as f:
    zip_data = f.read()

print(f"ZIP size: {len(zip_data)} bytes")

# העלה ל-Netlify
req = urllib.request.Request(
    'https://api.netlify.com/api/v1/sites',
    data=zip_data,
    headers={'Content-Type': 'application/zip'},
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
        url = f"https://{data['subdomain']}.netlify.app"
        print(f"\n✅ האתר עלה בהצלחה!")
        print(f"🌐 כתובת: {url}")
        print(f"ID: {data['id']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Error {e.code}: {body}")
