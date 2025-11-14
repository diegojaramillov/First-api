import json
import urllib.request

url='http://127.0.0.1:5000/auth/login'
data=json.dumps({'username':'admin','password':'admin123'}).encode()
req=urllib.request.Request(url,data=data,headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req) as r:
    print(r.read().decode())
