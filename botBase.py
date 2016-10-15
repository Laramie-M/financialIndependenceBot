import praw
import sqlite3

def opendb():
    #opens db and returns a cursor object
    connect = sqlite3.connect('example.db')
    return connect.cursor()


def main():
    db = opendb()
    db.execute('''CREATE TABLE user (id text, displayName text, firstPost text)''')

main()
