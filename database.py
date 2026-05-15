import sqlite3

def init_db():
    conn = sqlite3.connect('support.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            message_id_in_group INTEGER
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_langs (
            user_id INTEGER PRIMARY KEY,
            lang TEXT DEFAULT 'ru'
        )
    ''')
    conn.commit()
    conn.close()

def save_message(user_id, username, message_id_in_group):
    conn = sqlite3.connect('support.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO messages (user_id, username, message_id_in_group) VALUES (?, ?, ?)',
                (user_id, username, message_id_in_group))
    conn.commit()
    conn.close()

def get_user_by_group_message(message_id_in_group):
    conn = sqlite3.connect('support.db')
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM messages WHERE message_id_in_group = ?', (message_id_in_group,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def set_user_lang(user_id, lang):
    conn = sqlite3.connect('support.db')
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO user_langs (user_id, lang) VALUES (?, ?)', (user_id, lang))
    conn.commit()
    conn.close()

def get_user_lang(user_id):
    conn = sqlite3.connect('support.db')
    cur = conn.cursor()
    cur.execute('SELECT lang FROM user_langs WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 'ru'