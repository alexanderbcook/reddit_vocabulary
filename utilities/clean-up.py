import redis
import psycopg2
from psycopg2.extensions import AsIs

try:
    conn = psycopg2.connect("dbname='postgres' host ='localhost'")
except:
    print "Can't connect to PSQL!"

subreddits = ['politics','the_donald','worldnews','news']
cur = conn.cursor()

for subreddit in subreddits:
    cur.execute("DELETE FROM reddit.%s WHERE proportion < 0.00005;", (AsIs(subreddit),))
    message = cur.statusmessage.replace('DELETE ', '')
    print 'Deleted ' +  message + ' rows with a proportionality below threshold from reddit.'+subreddit + '.'

conn.commit()
cur.close()
conn.close()