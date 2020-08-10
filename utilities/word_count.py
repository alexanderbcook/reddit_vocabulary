import redis
import psycopg2
from psycopg2.extensions import AsIs
import datetime

try:
    redis = redis.StrictRedis(host='localhost', port=6379, db=0)
except:
    print "Can't connect to Redis!"

try:
    conn = psycopg2.connect("dbname='postgres'")
except:
    print "Can't connect to PSQL!"

subreddits = ['politics','worldnews','news']
date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

cur = conn.cursor()

for subreddit in subreddits:
    i = redis.llen(subreddit)
    while i > 0:
        word = redis.lpop(subreddit)
        cur.execute("INSERT INTO reddit.%s AS s (word, count, full_date, day) VALUES (%s, %s, %s, date_trunc('day', %s::date)) ON CONFLICT ON CONSTRAINT %s_word_day DO UPDATE SET count = s.count + 1",
                    (AsIs(subreddit), word, 1, date, date, AsIs(subreddit)))
        i = i - 1

conn.commit()
cur.close()
conn.close()

