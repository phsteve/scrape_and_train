#!usr/bin/python

# Coded by Stephen Katz, 2013

# Scrapes the top news articles from reddit.com/r/news rss feed. Saves the articles
# into a folder named "html_docs" in the corrent directory. train.py then uses these html
# files to train a Bayes classifier

import os
from bs4 import BeautifulSoup
import requests
import feedparser
import sys

html_dir = os.path.join(os.path.dirname(__file__), 'html_docs')

def main(url):
    feed = feedparser.parse(str(url))

    all_links = ''.join([entry.summary for entry in feed.entries])
    news_links = {}

    soup = BeautifulSoup(all_links)

    for link in soup('a'):
        print link
        if link.text == '[link]':
            news_links[link.get('href')] = False

    for link in news_links:
        snippet_soup = BeautifulSoup(requests.get(link).text[:1000])

        if 'xmlns:og' in snippet_soup('html')[0].attrs:
            news_links[link] = True

    def dl(link):
        html = requests.get(link).text.encode('utf-8')
        soup = BeautifulSoup(html)
        f = open(os.path.join(html_dir, '-'.join(soup.title.text.split()) + '.html'), 'w')
        f.write(html)
        f.close()

    for link in news_links.keys():
        if news_links[link]:
            dl(link)

if __name__ == '__main__':
    main('http://reddit.com/r/news/.rss')