import sqlite3
import praw


def opendb(name):
    # opens db and returns a cursor object
    name = checkName(name)
    connect = sqlite3.connect(name)
    return connect, connect.cursor()


def checkName(name):
    # Receives a string checks for ending in .db
    if len(name) < 3:
        raise NameError
    elif name[-3:] != ".db":
        return name + ".db"
    else:
        return name

def adduser(c,ident,displayname):
    # receives a cursor object and user info and inserts into db
    try:
        c.execute('''INSERT INTO users (id, displayName) VALUES (?,?) ''',
                  (ident, displayname))
        print("User Added:", displayname)
    except sqlite3.IntegrityError as e:
        print("Couldn't add user:", displayname)
        print(" User already exists.")
        print()


def save(connect):
    # Receives db connection object and saves the db
    connect.commit()
    connect.close()

def redditConnect():
    r = praw.Reddit()
    r.login()

def main():
    connection, db = opendb("finI2.db")
    db.execute('''CREATE TABLE  IF NOT EXISTS
                    users (id integer PRIMARY KEY UNIQUE, displayName text, firstPost text)''')
    save(connection)


main()
