import math
import os

def createARFFFiles():

    #data_map = {date: {"jap_yen": 0, "euro": 0, "bitcoin": 0} }

    data_map = {}
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
            date = correctDate(date, False)
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
            date = correctDate(date, False)
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
            date = correctDate(date, False)
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
            date = correctDate(date, False)
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
            date = correctDate(date, False)
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
            date = correctDate(date, False)
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
            date = correctDate(date, False)
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
            date = correctDate(date, False)
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
            date = correctDate(date, False)
            price = split[1].rstrip()
            if date in data_map:
                data_map[date]["hkd"] = price

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
            date = correctDate(date, True)
            #print(new_date_string)
            price = split[4]
            if date in data_map:
                data_map[date]["bitcoin"] = price

    print(data_map) 

    training_index = int(math.ceil(len(dates)*.7))
    training_dates = dates[:training_index]
    testing_dates = dates[training_index:]

    variable_order = ["jap_yen", "euro", "bitcoin"]


    
    #Training Data
    f = open("../data/training.arff", "w")

    f.write("@Relation TRAINING\n\n")
    last_key = ""
    for v in variable_order:
        if(v == "dates"):
            f.write("@ATTRIBUTE " + v + " DATE " + "\"MM-dd-yyyy\"\n")
        else:
            f.write("@ATTRIBUTE " + v + " NUMERIC\n")
        last_key = v
    f.write("\n@DATA\n")

    for date in training_dates:
        for v in variable_order:
            f.write(str(data_map[date][v]))
            if(v != last_key):
                f.write(",")
        f.write("\n")
    
    f.close()

    #Testing Data
    f = open("../data/testing.arff", "w")
    f.write("@Relation TESTING\n\n")
    last_key = ""
    for v in variable_order:
        if(v == "dates"):
            f.write("@ATTRIBUTE " + v + " DATE " + "\"MM-dd-yyyy\"\n")
        else:
            f.write("@ATTRIBUTE " + v + " NUMERIC\n")
        last_key = v
    f.write("\n@DATA\n")

    for date in testing_dates:
        for v in variable_order:
            f.write(str(data_map[date][v]))
            if(v != last_key):
                f.write(",")
        f.write("\n")
    
    f.close()

def correctDate(old_date, IS_BITCOIN):
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

def runLinearRegression():
    command = "java -cp ../weka.jar weka.classifiers.functions.LinearRegression -t ../data/training.arff -T ../data/testing.arff -additional-stats > ../data/output/regression_output.out"
    os.system(command)

if __name__ == "__main__":
    createARFFFiles()
  #  runLinearRegression()


