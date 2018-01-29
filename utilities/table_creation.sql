CREATE TABLE reddit.politics (id serial PRIMARY KEY,word varchar, count integer, day timestamp, CONSTRAINT politics_word_day UNIQUE(word,day));
CREATE TABLE reddit.the_donald (id serial PRIMARY KEY, word varchar , count integer, day timestamp,CONSTRAINT the_donald_word_day UNIQUE(word,day));
CREATE TABLE reddit.news (id serial PRIMARY KEY, word varchar , count integer, day timestamp,CONSTRAINT news_word_day UNIQUE(word,day));
CREATE TABLE reddit.worldnews (id serial PRIMARY KEY, word varchar , count integer, day timestamp,CONSTRAINT worldnews_word_day UNIQUE(word,day));
