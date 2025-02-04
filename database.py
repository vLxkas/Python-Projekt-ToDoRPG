# database.py
import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            race TEXT,
            class TEXT,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            xp_to_next_level INTEGER DEFAULT 100
        )
    ''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            difficulty TEXT,
            deadline DATE,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()  
    conn.close()  

def insert_user(name, race, character_class):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, race, class) VALUES (?, ?, ?)', (name, race, character_class))
    conn.commit()  
    conn.close()  

def insert_quest(user_id, name, difficulty, deadline, status='open'):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO quests (user_id, name, difficulty, deadline, status) VALUES (?, ?, ?, ?, ?)',
                   (user_id, name, difficulty, deadline, status))
    conn.commit()  
    conn.close()  

def load_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')  
    users = cursor.fetchall()  
    conn.close()  
    return users  

def load_quests(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quests WHERE user_id = ?', (user_id,))  
    quests = cursor.fetchall()  
    conn.close()  
    return quests  

def update_quest_status(quest_id, status):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE quests SET status=? WHERE id=?', (status, quest_id))
    conn.commit()  
    conn.close()  

def delete_quest(quest_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM quests WHERE id=?', (quest_id,))
    conn.commit()  
    conn.close()  

def update_user_xp_and_level(user_id, xp, level, xp_to_next_level):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE users SET xp=?, level=?, xp_to_next_level=? WHERE id=?',
        (xp, level, xp_to_next_level, user_id)
    )
    conn.commit()  
    conn.close()  