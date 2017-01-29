import redis
import psycopg2
from psycopg2.extensions import AsIs
import datetime


try:
    conn = psycopg2.connect("dbname='postgres' host ='localhost'")
except:
    print "Can't connect to PSQL!"

d = 'the_donald'
n = 'news'
p = 'politics'
w = 'worldnews'

subreddits = ['politics','the_donald','worldnews','news']
word = 'fuck'
date = '2016-28-01'
cur = conn.cursor()

for subreddit in subreddits:

    cur.execute("SELECT count FROM reddit.%s;", (AsIs(subreddit),))

    values = []
    for value in cur.fetchall():
        values.append(value[0])
        total = sum(values)

    cur.execute("SELECT * FROM reddit.%s", (AsIs(subreddit),))
    for value in cur.fetchall():
        word = value[0]
        date = value[3]
        proportion = round(float(value[1])/float(total), 5)
        cur.execute("UPDATE reddit.%s SET proportion = %s WHERE word = %s AND day = %s", (AsIs(subreddit), proportion, word, date))

conn.commit()
cur.close()
conn.close()