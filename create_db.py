import sqlite3
from prettytable import PrettyTable
from prettytable import *
import json
import os


def create_db():
    conn = sqlite3.connect('endgame_database.db')

    conn.execute("""CREATE TABLE IF NOT EXISTS endgame_database (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        METHOD TEXT,
        URL TEXT, 
        PARAMS TEXT,
        REQUEST_BODY TEXT, 
        HEADERS TEXT,
        STATUS_CODE TEXT,
        RESPONCE TEXT)""")

    conn.close()


def insert(method, url, params, requests_body, headers, status, responce):
    conn = sqlite3.connect('endgame_database.db')
    conn.execute('''INSERT INTO endgame_database (METHOD, URL, PARAMS, REQUEST_BODY, HEADERS, STATUS_CODE, RESPONCE)
                 VALUES(?, ?, ?, ?, ?, ?, ?)''',
                 (method, url, params, requests_body, headers, status, responce))

    conn.commit()
    conn.close()


def show_db():
    usage_list = ['"usage" -- show usage list', '"show 1, 2, 3..." / "full show" -- shows FULL table by id',
                  '"q" -- Quit from CLI', ]
    conn = sqlite3.connect('endgame_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, METHOD, URL, PARAMS, REQUEST_BODY, STATUS_CODE FROM endgame_database')

    cols = ['id', 'Method', 'URL', 'Parameters', 'Request Body', 'Status Code']
    x = PrettyTable(cols)

    for i in cursor:
        x.add_row(i)

    print(x)

    while True:
        flag = input('Enter "usage" to inspect commands: ')
        if flag == 'q':
            break
        elif flag == 'full show':
            try:
                flag_index = int(input('Enter index: '))
                top = cursor.execute('''SELECT id, METHOD, URL, PARAMS, HEADERS, REQUEST_BODY, STATUS_CODE FROM 
                                                endgame_database WHERE id=?''', (int(flag_index), ))

                pretty_top_cols = ['id', 'Method', 'URL', 'Parameters', 'Headers', 'Request Body', 'Status Code']
                pretty_bot_cols = ['Response']
                pretty_top = PrettyTable(pretty_top_cols)
                pretty_bot = PrettyTable(pretty_bot_cols)

                for i in top:
                    pretty_top.add_row(i)

                bottom = cursor.execute('SELECT RESPONCE FROM endgame_database WHERE id=?', (int(flag_index),))
                print(pretty_top)
                print('---Response---')
                for i in bottom:
                    pretty_bot.add_row(i)

                print(pretty_bot)
            except Exception:
                print('Enter correct value.')
        elif flag == 'usage':
            for i in usage_list:
                print(i)
        elif flag == 'show':
            flag_id = int(input('Enter table id: '))
            cursor.execute('SELECT RESPONCE FROM endgame_database WHERE id=?', (int(flag_id), ))
            response_result = cursor.fetchall()
            print('---Response---')
            print(response_result)
        elif flag == 'delete by id':
            flag_id = int(input('Enter table id: '))
            cursor.execute('DELETE FROM endgame_database WHERE id=?', (int(flag_id), ))
            conn.commit()
        elif flag == 'delete table':
            cursor.execute('DELETE FROM endgame_database')
            conn.commit()
        else:
            print('Enter correct command.')


def clear_db():
    if os.path.exists('endgame_database.db'):
        conn = sqlite3.connect('endgame_database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM endgame_database')
        conn.commit()
        os.remove('endgame_database.db')
        return 'The database has been cleared.'
    else:
        return 'Database doesn\'t exist.'


def show_raw():
    conn = sqlite3.connect('endgame_database.db')
    cursor = conn.cursor()
    id = int(input('Enter table id: '))
    cursor.execute('SELECT RESPONCE FROM endgame_database WHERE id=?', (id, ))
    temp = cursor.fetchall()
    print('---Response---')
    for i in temp:
        for j in i:
            print(j)
