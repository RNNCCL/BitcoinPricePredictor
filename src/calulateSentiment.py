import os
import sys
import ast
from textblob import TextBlob

reload(sys)
sys.setdefaultencoding('utf8')

def getSentiment(tweet):
    blob = TextBlob(tweet)
    return blob.sentiment.polarity


directory = "./data/data_bitcoinmarkets/"

data = {}

for file in os.listdir(directory):
    s = open(directory + file, 'r').read()
    d= ast.literal_eval(s)
    for date in d:
    	if date not in data:
    		data[date] = {"sentiment": 0, "count": 0}
    	for post in d[date]:
    		sentiment = getSentiment(post[0])
    		data[date]["sentiment"] += sentiment
    		data[date]["count"] += 1
    		for comment in d[date][post]:
    			sentiment = getSentiment(comment)
	    		data[date]["sentiment"] += sentiment
	    		data[date]["count"] += 1

for date in data:
	data[date]["sentiment"] /= data[date]["count"]

print data
