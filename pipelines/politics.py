# !/usr/bin/python
import sys
sys.path.append('/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
import praw
import os
import re
import redis
from textblob import TextBlob
sys.path.append('/Users/alexandercook/Repositories/reddit_vocabulary/utilities')
import config
from config import *
import common_words
from common_words import words

# Login to reddit object
reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, password=config.password, user_agent=config.user_agent, username=config.username)
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
subreddit = reddit.subreddit('politics')

# Define pre-processing function

def preprocess_comment(str):
    str = str.decode("utf-8")
    str = str.replace(u"\u201c", "").replace(u"\u201d", "").replace('.','').replace("'",'')

    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
    str = emoji_pattern.sub(r'', str) 

    if '_' in str:
        return
    if '/' in str:
        return
    if "'" in str:
        return
    if ".com" in str:
        return
    if 'http' in str:
        return
    return str


# Define function to check comment id versus a list of processed comment ids and store new comments

def store_new_comments(comment, file, comment_list):
   if comment.id not in open(file).read():
    with open(file, "a") as text_file:
        text_file.write(comment.id)
        text_file.write('\n')
    comment_list.append((comment.body).lower()) 
    return comment_list

# Iterate through the top ten submissions, flatten all comments.

comments = []

for submission in subreddit.top('day', limit=25):
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        store_new_comments(top_level_comment, "temp/politics.txt", comments)
        for second_level_comment in top_level_comment.replies:
            store_new_comments(second_level_comment, "temp/politics.txt", comments)


# Process comments and add them to a cleaned list.

processed_words = []

for comment in comments:
    blob = TextBlob(comment)
    words = blob.words.singularize()

    for word in words:
        word = word.encode('utf-8')
        processed_word = preprocess_comment(word)
        if processed_word != None and processed_word not in common_words.words and len(processed_word) > 2:
            redis.lpush(subreddit, processed_word)
