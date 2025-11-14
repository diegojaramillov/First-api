import time
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE = 'http://127.0.0.1:5000'

def post(path, data, token=None):
    url = BASE + path
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
    try:
        with urlopen(req) as r:
            return r.getcode(), json.load(r)
    except HTTPError as e:
        try:
            payload = e.read().decode()
            return e.code, json.loads(payload)
        except:
            return e.code, e.reason

def get(path, token=None):
    url = BASE + path
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = Request(url, headers=headers, method='GET')
    try:
        with urlopen(req) as r:
            ct = r.getheader('Content-Type','')
            if 'application/json' in ct:
                return r.getcode(), json.load(r)
            return r.getcode(), r.read().decode()
    except HTTPError as e:
        try:
            payload = e.read().decode()
            return e.code, json.loads(payload)
        except:
            return e.code, e.reason

if __name__ == '__main__':
    print('Waiting 1s for server...')
    time.sleep(1)

    # Register a test admin user
    username = 'e2e_admin'
    password = 'admin123'
    code, res = post('/auth/register', {'username': username, 'password': password, 'role': 'admin'})
    print('REGISTER', code, res)

    # Login
    code, res = post('/auth/login', {'username': username, 'password': password})
    print('LOGIN', code, res)
    if code != 200:
        print('Login failed, aborting E2E')
        raise SystemExit(1)
    token = res.get('access_token')
    user = res.get('user')
    print('TOKEN:', bool(token), 'USER role:', user.get('role'))

    # Create a series
    code, res = post('/series/', {'title': 'E2E Series'}, token)
    print('CREATE SERIES', code, res)
    series_id = res.get('id') if isinstance(res, dict) else None

    # List series
    code, res = get('/series/', token)
    print('LIST SERIES', code, res)

    # Update series
    if series_id:
        code, res = post(f'/series/{series_id}', {'title': 'Should not use POST'}, token)
        print('UPDATE (wrong method) expected 405/405-like', code, res)
        # Use PUT
        import urllib.request
        url = f'{BASE}/series/{series_id}'
        headers = {'Content-Type':'application/json', 'Authorization': f'Bearer {token}'}
        req = Request(url, data=json.dumps({'title':'E2E Series Updated'}).encode('utf-8'), headers=headers, method='PUT')
        try:
            with urlopen(req) as r:
                print('PUT update', r.getcode(), json.load(r))
        except HTTPError as e:
            print('PUT update failed', e.code, e.read().decode())

        # Delete
        req = Request(f'{BASE}/series/{series_id}', headers={'Authorization': f'Bearer {token}'}, method='DELETE')
        try:
            with urlopen(req) as r:
                print('DELETE', r.getcode(), json.load(r))
        except HTTPError as e:
            try:
                print('DELETE failed', e.code, json.loads(e.read().decode()))
            except:
                print('DELETE failed', e.code, e.reason)

    print('E2E test finished')
