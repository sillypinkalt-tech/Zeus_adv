# Database initialization
import sqlite3

def init_db():
    conn = sqlite3.connect('zeus_adv.db')
    cur = conn.cursor()
    cur.execute(''
        CREATE TABLE IF NOT EXISTS subscriptions ("
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            plan_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        )
    '')
    cur.execute(''
        CREATE TABLE IF NOT EXISTS keys ("
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            user_id TEXT NULL,
            plan_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NULL
        )
    '')
    cur.execute(''
        CREATE TABLE IF NOT EXISTS campaigns ("
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            sending_account TEXT NOT NULL,
            channels TEXT NOT NULL,
            message TEXT NOT NULL,
            interval INT NOT NULL,
            status TEXT NOT NULL DEFAULT 'stopped'
        )
    '')
    conn.commit()
    cur.close()
    conn.close()
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('zeus_adv.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(''
        CREATE TABLE IF NOT EXISTS subscriptions ("
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            plan_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        )
    '')
    cur.execute(''
        CREATE TABLE IF NOT EXISTS keys ("
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            user_id TEXT NOT NULL,
            plan_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        )
    '')
    cur.execute(''
        CREATE TABLE IF NOT EXISTS campaigns ("
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            sending_account TEXT NOT NULL,
            channels TEXT NOT NULL,
            message TEXT NOT NULL,
            interval INT NOT NULL,
            status TEXT NOT NULL DEFAULT 'stopped'
        )
    '')
    conn.commit()
    cur.close()
    conn.close()