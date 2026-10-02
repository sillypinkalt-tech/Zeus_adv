import sqlite3
import random
import string
from datetime import datetime, timedelta

def generate_key(plan_type):
    conn = sqlite3.connect('zeus_adv.db')
    cur = conn.cursor()
    
    while True:
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        cur.execute('SELECT * FROM keys WHERE key = ?', (key,))
        if not cur.fetchone():
            # Store as pending with no expiration
            cur.execute(''
                INSERT INTO keys (key, plan_type)
                VALUES (?, ?)
            '', (key, plan_type))
            conn.commit()
            cur.close()
            conn.close()
            return key
        cur.close()
        conn.close()
import sqlite3
import random
import string
from datetime import datetime, timedelta

def generate_key(plan_type):
    while True:
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        conn = sqlite3.connect('zeus_adv.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM keys WHERE key = ?', (key,))
        if not cur.fetchone():
            now = datetime.now()
            expires = now + timedelta(days=30)
            cur.execute(''
                INSERT INTO keys (key, user_id, plan_type, expires_at)
                VALUES (?, ?, ?, ?)
            '', (key, 'pending', plan_type, expires))
            conn.commit()
            cur.close()
            conn.close()
            return key
        cur.close()
        conn.close()