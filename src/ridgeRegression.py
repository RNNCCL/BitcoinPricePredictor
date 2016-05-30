import math
import os
import numpy as np

from scipy import stats
import matplotlib.pyplot as plt
from sklearn.linear_model import BayesianRidge, LinearRegression
from sklearn.svm import SVR
from sklearn import datasets, linear_model
from sklearn import ensemble
from math import ceil
from math import floor
from scipy.stats import spearmanr

import collections


def gather_data():

    # data_map = {}
    data_map = collections.OrderedDict()
    dates = []
    #jap_yen
    with open("../data/japyen_price.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            price = split[1].rstrip()
            date = correct_date(date, False)
            if date not in data_map:
                data_map[date] = {
                    "jap_yen": price, 
                    "yuan": -1, 
                    "riyal": -1, 
                    "rouble": -1, 
                    "euro": -1, 
                    "pound": -1, 
                    "koruna": -1, 
                    "franc": -1, 
                    "hkd": -1, 
                    "trans":0,
                    "sentiment": 0,
                    "sentiment2": 0,
                    "bitcoin": -1
                }
                dates.append(date)

    with open("../data/euro_price.csv") as f1:
        first_line = True
        for line in f1:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["euro"] = price

    with open("../data/yuan_price.csv") as f2:
        first_line = True

        for line in f2:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["yuan"] = price
            

    with open("../data/riyal_price.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["riyal"] = price

    with open("../data/rouble_price.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["rouble"] = price

    with open("../data/pound_price.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["pound"] = price

    with open("../data/koruna_price.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["koruna"] = price

    with open("../data/franc_price.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["franc"] = price

    with open("../data/hkd_price.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["hkd"] = price

    with open("../data/num_transactions_per_day.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0].split()[0]
            date = correct_date(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["trans"] = price

    with open("./data_sentiment/sentiment_by_date.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date_sentiment(date, True)
            sentiment = split[1].rstrip()
            if date in data_map:
                data_map[date]["sentiment"] = sentiment

    with open("./data_sentiment/r_bitcoin_sentiment_by_date.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0]
            date = correct_date_sentiment(date, True)
            sentiment = split[1].rstrip()
            if date in data_map:
                data_map[date]["sentiment2"] = sentiment

    with open("../data/bitcoin_price.csv") as f:
        first_line = True
        for line in f:
            if(first_line):
                first_line = False
                continue
            split = line.split(",")
            date = split[0].rstrip()
            date_split = date.split(" ")
            date = date_split[0]
            date = correct_date(date, True)
            #print(new_date_string)
            price = split[4]
            if date in data_map:
                data_map[date]["bitcoin"] = price

    # print(data_map)

    for key in data_map.keys():
        currencies = data_map[key]
        if -1 in currencies.values():
            del data_map[key]
    return(data_map)

def organize_data_correlate(data_map):
    feature_array = []
    label_array = []
    for date,val in data_map.iteritems():
        franc = float(val["franc"])
        yuan =  float(val["yuan"])
        hkd = float(val["hkd"])
        euro = float(val["euro"])
        koruna = float(val["koruna"])
        jap_yen = float(val["jap_yen"])
        pound = float(val["pound"])
        bitcoin = float(val["bitcoin"])
        riyal = float(val["riyal"])
        rouble = float(val["rouble"])

        # print(riyal)

        if(franc == 0 or yuan == 0 or hkd == 0 or euro == 0 or koruna == 0 or jap_yen == 0 or pound == 0 or riyal == 0 or rouble == 0):
            continue

        if(bitcoin > 100000):
            continue

        features = (franc, yuan, hkd, euro, koruna, jap_yen, pound, riyal, rouble)
        feature_array.append(features)
        label_array.append(bitcoin)

    print("feature_array size:",len(feature_array))
    print("label_array size:",len(label_array))

    return (feature_array, label_array)


def organize_data_predict(data_map):
    feature_array = []
    label_array = []

    yesterday_franc = -1
    yesterday_yuan =  -1
    yesterday_hkd = -1
    yesterday_euro = -1
    yesterday_koruna = -1
    yesterday_jap_yen = -1
    yesterday_pound = -1
    yesterday_bitcoin = -1
    yesterday_riyal = -1
    yesterday_rouble = -1
    yesterday_sentiment = 0
    yesterday_sentiment2 = 0
    yesterday_trans = 0

    for date,val in data_map.iteritems():
        franc = float(val["franc"])
        yuan =  float(val["yuan"])
        hkd = float(val["hkd"])
        euro = float(val["euro"])
        koruna = float(val["koruna"])
        jap_yen = float(val["jap_yen"])
        pound = float(val["pound"])
        bitcoin = float(val["bitcoin"])
        riyal = float(val["riyal"])
        rouble = float(val["rouble"])
        sentiment_val = float(val["sentiment"])
        sentiment2_val = float(val["sentiment2"])
        trans_num = float(val["trans"])

        # print(riyal)

        if(franc == 0 or yuan == 0 or hkd == 0 or euro == 0 or koruna == 0 or jap_yen == 0 or pound == 0 or riyal == 0 or rouble == 0):
            continue

        if(bitcoin > 100000):
            print bitcoin
            continue

        if(yesterday_bitcoin == -1 or yesterday_jap_yen == -1):
            yesterday_franc = franc
            yesterday_yuan =  yuan
            yesterday_hkd = hkd
            yesterday_euro = euro
            yesterday_koruna = koruna
            yesterday_jap_yen = jap_yen
            yesterday_pound = pound
            yesterday_bitcoin = bitcoin
            yesterday_riyal = riyal
            yesterday_rouble = rouble
            yesterday_sentiment = sentiment_val
            yesterday_sentiment2 = sentiment2_val
            yesterday_trans = trans_num
            continue

        # features = (yesterday_franc, yesterday_yuan, yesterday_hkd, 
        #     yesterday_euro, yesterday_koruna, yesterday_jap_yen, 
        #     yesterday_pound, yesterday_riyal, yesterday_rouble, yesterday_trans,
        #     yesterday_sentiment, yesterday_sentiment2, yesterday_bitcoin)

        features = (yesterday_hkd, 
            yesterday_rouble, yesterday_trans,
            yesterday_sentiment, yesterday_sentiment2, yesterday_bitcoin)

        # features = (yesterday_bitcoin, 0)

        feature_array.append(features)
        label_array.append(bitcoin)

        yesterday_franc = franc
        yesterday_yuan =  yuan
        yesterday_hkd = hkd
        yesterday_euro = euro
        yesterday_koruna = koruna
        yesterday_jap_yen = jap_yen
        yesterday_pound = pound
        yesterday_bitcoin = bitcoin
        yesterday_riyal = riyal
        yesterday_rouble = rouble
        yesterday_sentiment = sentiment_val
        yesterday_sentiment2 = sentiment2_val
        yesterday_trans = trans_num

    print("feature_array size:",len(feature_array))
    print("label_array size:",len(label_array))

    return (feature_array, label_array)


def correct_date(old_date, IS_BITCOIN):
        new_date_string = ""

        split_date = old_date.split("/")
        if(len(split_date[1]) == 1):
            split_date[1] = "0" + split_date[1]
        if(len(split_date[0]) == 1):
            split_date[0] = "0" + split_date[0]
        if(len(split_date[2]) != 4):
            split_date[2] = "20" + split_date[2]

        if(IS_BITCOIN):
            new_date_string = split_date[0] + "/" + split_date[1] + "/" + split_date[2]
        else:
            new_date_string = split_date[1] + "/" + split_date[0] + "/" + split_date[2]

        return new_date_string

def correct_date_sentiment(old_date, IS_BITCOIN):
        new_date_string = ""

        split_date = old_date.split("-")
        if(len(split_date[1]) == 1):
            split_date[1] = "0" + split_date[1]
        if(len(split_date[0]) == 1):
            split_date[0] = "0" + split_date[0]
        if(len(split_date[2]) != 4):
            split_date[2] = "20" + split_date[2]

        if(IS_BITCOIN):
            new_date_string = split_date[0] + "/" + split_date[1] + "/" + split_date[2]
        else:
            new_date_string = split_date[1] + "/" + split_date[0] + "/" + split_date[2]

        return new_date_string


def bayesian_ridge_regression(feature_array, label_array):
    clf = BayesianRidge(compute_score=True)
    clf.fit(feature_array, label_array)

    ols = LinearRegression()
    ols.fit(feature_array, label_array)


    n_features = 9

    plt.figure(figsize=(6, 5))
    plt.title("Weights of the model")
    plt.plot(clf.coef_, 'b-', label="Bayesian Ridge estimate")
    plt.plot(label_array, 'g-', label="Ground truth")
    plt.plot(ols.coef_, 'r--', label="OLS estimate")
    plt.xlabel("Features")
    plt.ylabel("Values of the weights")
    plt.legend(loc="best", prop=dict(size=12))

    plt.figure(figsize=(6, 5))
    plt.title("Histogram of the weights")
    plt.hist(clf.coef_, bins=n_features, log=True)
    # plt.plot(clf.coef_[feature_array], 5 * np.ones(len(feature_array)),
    #          'ro', label="Relevant features")
    plt.ylabel("Features")
    plt.xlabel("Values of the weights")
    plt.legend(loc="lower left")

    plt.figure(figsize=(6, 5))
    plt.title("Marginal log-likelihood")
    plt.plot(clf.scores_)
    plt.ylabel("Score")
    plt.xlabel("Iterations")
    plt.show()

def cal_correlation(x,y):
    rank_correlation = spearmanr(x, y)[0]
    return rank_correlation

def mean_average_error(predicted_labels, actual_labels):
    i = 0
    mae = 0
    while i < len(predicted_labels):
        mae += abs(predicted_labels[i] - actual_labels[i])
        i += 1

    return mae/len(predicted_labels)

def mean_square_error(predicted_labels, actual_labels):
    i = 0
    mse = 0
    while i < len(predicted_labels):
        mse += pow(abs(predicted_labels[i] - actual_labels[i]),2)
        i += 1

    return mse/len(predicted_labels)


def random_forest(feature_array, label_array):
    # print("feature_array:",feature_array)
    train = int(floor(0.8*len(feature_array)))
    print 'Training with',train,'samples'
    
    # Random forest model
    rf = ensemble.RandomForestRegressor(n_estimators=100)
    rf.fit(feature_array[:train], label_array[:train])
    print'Built random forest and trained it'

    # Linear regression
    regr = linear_model.LinearRegression()
    regr.fit(feature_array[:train], label_array[:train])
    print'Built Linear'

    # SVR
    clf = SVR()
    clf.fit(feature_array[:train], label_array[:train])
    print'Built SVR'


    feature_pass_array = feature_array[train:]
    label_pass_array = label_array[train:]

    # predict_labels_2 = ((0.98137,6.5388,7.764525,0.886093,23.94465,109.635,0.68358,3.75025,65.2635),(0.972585,6.5002,7.7612,0.876885,23.6973,107.1085,0.693005,3.75025,65.879))
    # Features for 5/4/16 - the day after our training stops.
    # predict_labels_2 = ((0.99024,6.5467,7.7668,0.89102,24.082,110.255,0.6866,3.7516,66.8665,442.99),(0,0,0,0,0,0,0,0,0,0)) 
    
    # Random forest
    # predicted_rf = rf.predict(predict_labels_2)
    # print("Predicted RF:",predicted_rf)

    # SVR
    # predicted_clf = clf.predict(predict_labels_2)
    # print("Predicted SVR:",predicted_clf)

    # Linear regression
    # predict_labels = regr.predict(feature_pass_array)
    # print("Predicted Linear:",predicted_linear)


    # Important features
    print "Important features:"
    print rf.feature_importances_


    # Complete dataset
    predict_labels = rf.predict(feature_pass_array)
    # predict_labels = rf.predict(predict_labels_2)
    i = 0
    fuckup_count = 0
    while i<len(predict_labels):
        fucked = abs(predict_labels[i]) - label_pass_array[i]
        if(fucked > 10):
            fuckup_count += 1
            print ("fuckup: ", fucked, predict_labels[i], label_pass_array[i])
        # print "%8.4f ... %8.4f" % (predict_labels[i], label_pass_array[i])#str(predict_labels[i]) + " ... " + str(label_pass_array[i])
        i += 1


    rank_correlation = cal_correlation(label_pass_array,predict_labels)
    mae = mean_average_error(predict_labels, label_pass_array)
    mse = mean_square_error(predict_labels, label_pass_array)
    
    print '\nTraining done --------- '
    print 'Total samples:          ',len(feature_array)
    print 'Size of test data:      ',len(predict_labels)
    print 'Rank correlation:',rank_correlation
    print 'MAE:',mae
    print 'MSE:',mse
    print 'fuckup_count:',fuckup_count
    print '----------------------- \n'

if __name__ == "__main__":
    data_map = gather_data()

    # X, y = organize_data_correlate(data_map)
    # bayesian_ridge_regression(X, y)
    # random_forest(X, y)

    X, y = organize_data_predict(data_map)
    # bayesian_ridge_regression(X, y)
    random_forest(X, y)







