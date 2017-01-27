import redis
import psycopg2
from psycopg2.extensions import AsIs

try:
    redis = redis.StrictRedis(host='localhost', port=6379, db=0)
except:
    print "Can't connect to Redis!"

try:
    conn = psycopg2.connect("dbname='postgres' host ='localhost'")
except:
    print "Can't connect to PSQL!"

cur = conn.cursor()
subreddits = ['politics','the_donald','worldnews','news','upliftingnews']

for subreddit in subreddits:
    i = redis.llen(subreddit)
    while i > 0:
        word = redis.lpop(subreddit)
        cur.execute("INSERT INTO reddit.%s as s (word, count) VALUES (%s, %s) ON CONFLICT (word) DO UPDATE SET count = s.count + 1",
                    (AsIs(subreddit), word, 1))
        i = i - 1

conn.commit()

cur.close()
conn.close()

