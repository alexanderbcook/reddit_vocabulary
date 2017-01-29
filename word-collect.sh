#!/bin/bash

clear 
echo "Fetching r/politics posts..."
python pipelines/politics.py
echo "Done!"
echo "Fetching r/news posts..."
python pipelines/news.py
echo "Done!"
echo "Fetching r/worldnews posts..."
python pipelines/worldnews.py
echo "Done!"
echo "Fetching r/the_donald posts..."
python pipelines/the_donald.py
echo "Done!"
echo "Uploading word counts to PSQL..."
python utilities/word_count.py
echo "Done!"
echo "Calculating word proportionality..."
python utilities/proportion.py
echo "Script complete! Verify data integrity in PSQL."