#!/usr/bin/python

# Coded by Stephen Katz, 2013

# train.py takes a folder of html files (html_docs) and uses OpenGraph labels to
# train a Bayes classifier. This is part of a larger text classification project
# written by a friend of mine. The goal is to select elements of the DOM in news articles
# that are actual article content, versus the many other DOM elements that may have
# text in them but no article content (i.e. ads, links, summaries of other articles etc)

# It works well processing three or fewer articles, but more than that gives a
# "too many values to unpack" ValueError from the naivebayes module. Further exploration
# is necessary...

from nltk.classify import naivebayes
from bs4 import BeautifulSoup
from bs4.element import Tag
import os
import glob

html_dir = os.path.join(os.path.dirname(__file__), 'html_docs')

def open_html(filename):
    #print "opening html"
    f = open(filename, 'r')
    html = f.read()
    f.close()
    return html

def get_soup(html):
    #print "getting soup"
    dom = BeautifulSoup(html)
    return dom.find('body')

def traverse_dom(doms):
    #print "traversing dom"
    labeled_featuresets = []
    for dom in doms:
        for element in dom.find_all():
            if not isinstance(element, Tag):
                continue
            ##print element.name, element.attrs
            label = content_label(element)
            features = extract_element_features(element)
            labeled_featuresets.append((features, label))
    return labeled_featuresets

def content_label(element):
    #print "getting content labels"
    if 'articleContent' in element.get('class', []):
        return 'content'
    else:
        return 'garbage'

def text(element):
    #print "concatenating strings"
    return ''.join(x for x in element.stripped_strings)

def string_length(element):

    return len(text(element))

def extract_element_features(element):
    #print "extracting element features"
    features = {}
    total_length = string_length(element)
    link_length = sum(string_length(anchor) for anchor in [x for x in element('a')])

    features['low_link_density'] = ((link_length *1.0)/(total_length or 1) < .4)
        #true if link density is low, can play with < .4 to fine tune

    features['high_comma_count'] = (text(element).count(',') > 2)
        #true if there are more than 2 commas in the element

    features['high_word_count'] = (len(text(element).split(' ')) > 5)

    return features

def train_classifier(labeled_featuresets):
    #print "training classifier"
    trained_classifier = naivebayes.NaiveBayesClassifier.train(labeled_featuresets)
    return trained_classifier

if __name__ == '__main__':
    doms = []
    labeled_featuresets = []
    #print os.path.join('html_dir', '*.html')
    print glob.glob(os.path.join(html_dir, '*.html'))
    for html_file in glob.glob(os.path.join(html_dir, '*.html')):
        #html = open_html(os.path.join(html_dir, 'Ban-on-free-condoms-under-scrutiny-at-Boston-College---Salon.com.html')) #USE spider.py, 
        html = open_html
        dom = get_soup(open_html(html_file))
        doms.append(dom)
    print len(doms)
    #print doms
    #for dom in doms:
    labeled_featuresets.append(traverse_dom(doms))
    print labeled_featuresets
    #print labeled_featuresets
    trained_classifier = train_classifier(labeled_featuresets)
    trained_classifier.show_most_informative_features(n=10)