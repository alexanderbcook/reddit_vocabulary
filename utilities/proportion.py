import redis
import psycopg2
from psycopg2.extensions import AsIs

try:
    conn = psycopg2.connect("dbname='postgres' host ='localhost'")
except:
    print "Can't connect to PSQL!"

subreddits = ['politics','worldnews','news']
cur = conn.cursor()

for subreddit in subreddits:
    values = []

    cur.execute("SELECT count FROM reddit.%s;", (AsIs(subreddit),))
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
