import sqlite3


def __dict_factory(cur, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


connection = sqlite3.connect('db.sqlite3', check_same_thread=False)
connection.row_factory = __dict_factory

cursor = connection.cursor()
