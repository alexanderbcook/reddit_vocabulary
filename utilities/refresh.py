mport psycopg2
from psycopg2.extensions import AsIs

try:
    conn = psycopg2.connect("dbname='postgres'")
except:
    print "Can't connect to PSQL!"

subreddits = ['politics','the_donald','worldnews','news']
cur = conn.cursor()

for subreddit in subreddits:
    cur.execute("REFRESH MATERIALIZED VIEW day_%s", (AsIs(subreddit),))
    cur.execute("REFRESH MATERIALIZED VIEW month_%s", (AsIs(subreddit),))
    cur.execute("REFRESH MATERIALIZED VIEW year_%s", (AsIs(subreddit),))
    print "Finished refresh of materialized view for " + subreddit "."

conn.commit()
cur.close()
conn.close()
