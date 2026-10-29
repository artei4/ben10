import sqlite3
from pathlib import Path
import app as app_module

print('DB_EXISTS', Path('database/omnitrix.db').exists())
conn = sqlite3.connect('database/omnitrix.db')
print('TABLES', conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall())
conn.close()

app = app_module.app
app.config['TESTING']=True
client = app.test_client()
resp = client.post('/register', data={'username':'abc123','password':'1234'}, follow_redirects=False)
print('status', resp.status_code)
print('location', resp.headers.get('Location'))
print(resp.get_data(as_text=True)[:500])
