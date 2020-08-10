#/bin/bash

clear 
echo "Fetching r/politics posts..."
python /home/ec2-user/reddit_vocabulary/pipelines/politics.py
echo "Done!"
echo "Fetching r/news posts..."
python /home/ec2-user/reddit_vocabulary/pipelines/news.py
echo "Done!"
echo "Fetching r/worldnews posts..."
python /home/ec2-user/reddit_vocabulary/pipelines/worldnews.py
echo "Done"
echo "Uploading word counts to PSQL..."
python /home/ec2-user/reddit_vocabulary/utilities/word_count.py
echo "Done!"
python /home/ec2-user/reddit_vocabulary/utilities/clean-up.py
echo "Refreshing materialized views..."
python /home/ec2-user/reddit_vocabulary/utilities/refresh.py
echo "Script complete! Verify data integrity in PSQL."
