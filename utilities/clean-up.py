import redis
import psycopg2
import datetime
from psycopg2.extensions import AsIs

try:
    conn = psycopg2.connect("dbname='postgres'")
except:
    print "Can't connect to PSQL!"

subreddits = ['politics','worldnews','news']
cur = conn.cursor()

startDate = str(datetime.datetime.now() - datetime.timedelta(days=365))

for subreddit in subreddits:
    cur.execute("DELETE FROM reddit.%s WHERE count = 1;", (AsIs(subreddit),))
    message = cur.statusmessage.replace('DELETE ', '')
    print 'Deleted ' + message + ' rows with a proportionality below threshold from reddit.'+ subreddit + '.'
    print("DELETE FROM reddit.%s WHERE full_date <'"+startDate+"';")
    cur.execute("DELETE FROM reddit.%s WHERE full_date < '"+startDate+"';", (AsIs(subreddit),))
    message = cur.statusmessage.replace('DELETE ', '')
    print 'Deleted ' + message + ' rows that are older than ' + startDate + ' from reddit.' + subreddit + '.'

conn.commit()
cur.close()
conn.close()
