import os
import sys
import ast
from textblob import TextBlob

reload(sys)
sys.setdefaultencoding('utf8')

def getSentiment(tweet):
    blob = TextBlob(tweet)
    x = blob.sentiment.polarity
    #if(x>0.5):
     #   print blob + " \n!!!!! " + str(x) + "\n"
    return x


def get_subreddit_sentiment(directory, file_to_write, num_comments):
    data = {}
    write_data = {}
    for file in os.listdir(directory):
        # print "File name is : " + str(file)
        s = open(directory + file, 'r').read()
        d = ast.literal_eval(s)
        for date in d:
            # Add date to data array
            if date not in data:
                data[date] = {"sentiment": 0, "count": 0, "avg_sentiment": 0}
                write_data[date] = 0

            # Iterate through every submission of the date
            for post in d[date]:
                # Get the sentiment of the submission itself
                data[date]["sentiment"] += getSentiment(post[0]) * post[1]
                data[date]["count"] += abs(post[1])
                key = (post[0], post[1])

                # print "\n =========================="
                # print "The post : " + str(post[0])
                # print "Post has score of " + str(post[1]) + " and sentiment " + str(getSentiment(post[0]))
                # Get the sentiment of each comment to the submission
                comment_num = 0
                for comment in d[date][key]:
                    sentiment = getSentiment(comment)
                    comment_score = d[date][key][comment]
                    # print "------------"
                    # print "The comment : " + str(comment)
                    # print "The comment has score of " + str(comment_score) + " and sentiment " + str(sentiment)
                    data[date]["sentiment"] += sentiment * comment_score
                    data[date]["count"] += abs(comment_score)
                    if comment_num == num_comments:
                        break
                    comment_num += 1
                    

            # Get the average sentiment of the day
            if data[date]["count"] == 0:
                continue

            data[date]["avg_sentiment"] = data[date]["sentiment"] # / data[date]["count"]
            write_data[date] = data[date]["avg_sentiment"]
        #     break
        # break


    # print data

    # for date in data:
    #     if abs(data[date]["avg_sentiment"]) > .1:
    #         print date + " : " + str(data[date])

    print "Writing to file"
    f = open(file_to_write, "w")
    f.write("date,sentiment,\n")
    i = 0
    for date in write_data:
        f.write(date + "," + str(write_data[date]) + ",\n")
    f.close()


directory = "./data/data_bitcoinmarkets/"
file_to_write = "./data_sentiment/sentiment_by_date.csv"

get_subreddit_sentiment(directory, file_to_write, 3)

directory = "./data/data_r_bitcoin/"
file_to_write = "./data_sentiment/r_bitcoin_sentiment_by_date.csv"

get_subreddit_sentiment(directory, file_to_write, 3)

# for date in data:
#     data[date]["sentiment"] /= data[date]["count"]

# print data
