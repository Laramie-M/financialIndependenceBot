import sqlite3
import praw
import datetime


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
    r = praw.Reddit(client_id='3cysUO0CfofzUg',
                     client_secret=input("Input Secret:"),
                     user_agent='my user agent')
    return r

def checkedSubmission(id):
    return False

def submissionGathering(r):
    subreddit = r.subreddit('financialindependence')
    for submission in subreddit.new(limit=100):
        if checkedSubmission(submission.id):
            pass
        commentParsing(submission)

def commentParsing(submission):
    submission.comments.replace_more(limit=0)
    comment_queue = submission.comments.list()
    while comment_queue:
        comment = comment_queue.pop(0)
        print(comment.permalink())
        print(" Created: ",datetime.datetime.fromtimestamp(comment.created))
        print(" Author: ",comment.author)

def startUp():
    connection, db = opendb("FI_Users.db")
    db.execute('''CREATE TABLE  IF NOT EXISTS
                        users (id integer PRIMARY KEY UNIQUE, displayName text, firstPost text)''')
    r = redditConnect()
    submissionGathering(r)
    return connection



def main():
    connection = startUp()
    save(connection)


main()
