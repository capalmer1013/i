import sqlite3
import os
import getpass
from bcrypt import hashpw, gensalt

PLAYER_DB = 'players.db'
if not os.path.isfile(PLAYER_DB):
    open(PLAYER_DB, 'w+')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def createCharacterDb():
    conn = sqlite3.connect(PLAYER_DB)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE players
    (username text, password text, x integer, y integer, health real,
    item1 text, item2 text, item3 text, UNIQUE(username))
    ''')
    conn.commit()
    conn.close()


def removeAllPlayers():
    conn = sqlite3.connect(PLAYER_DB)
    c = conn.cursor()
    c.execute('''
    DELETE FROM players
    ''')
    conn.commit()
    conn.close()


def lookupUsernamePassword(username, password):
    conn = sqlite3.connect(PLAYER_DB)
    conn.row_factory = dict_factory
    c = conn.cursor()
    print username
    c.execute('''SELECT * FROM players WHERE username=?''', (username,))
    result = c.fetchone()
    conn.close()

    if not result:
        return False
    hashed = str(result['password'])
    if hashpw(password, hashed) == hashed:
        return True

    return False


def createUsernamePassword(username, password):
    conn = sqlite3.connect(PLAYER_DB)
    c = conn.cursor()
    values = (username, hashpw(password, gensalt(13)), -1, -1, 100.0, '', '', '')
    try:
        c.execute('''
        INSERT INTO players
        VALUES(?, ?, ?, ?, ?, ?, ?, ?);
        ''', values)
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return "Username probably taken"

    except Exception as e:
        return "Broken", e

    return "success"

if __name__ == "__main__":
    # createCharacterDb()
    user = raw_input("username: ")
    password = getpass.getpass("password: ")
    #createUsernamePassword(user, password)
    a = "success" if lookupUsernamePassword(user, password) else "you messed up"
    print a
    #removeAllPlayers()
