#======================================================================
# Author: Karen Ng <karenyng@ucdavis.edu>
# Date: 03/16/2014
# Winter 14 Stat 250 HW 3
# "prototype" code for classifying SO questions
#======================================================================
from __future__ import division
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# homebrewed module from path
sys.path.append('../writeup/')
import helper
import datetime

#-----initialize values------------------------------------------------
train_file = "../data/train-sample.csv"
test_file = "../data/train.csv"
date1 = "OwnerCreationDate"
date2 = "PostCreationDate"
dateDiff = "postOwnerTimeDiff"
output_file = "RF_" + str(datetime.datetime.now()) + ".txt"

criterion = 'gini'
max_features = "sqrt"
binaryClass = True

# initialize list of strings of variables to be used for RF
var = [dateDiff,
       "ReputationAtPostCreation",
       "OwnerUndeletedAnswerCountAtPostTime",
       "OwnerUserId",
       "PostId"]
status = \
    ["not constructive", "off topic", "not a real question", "too localized"]

#----------------------------------------------------------------------
# read in and preprocess data
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)
train = \
    helper.get_timeStamp_and_compute_date_diff(train, date1, date2, dateDiff)
test = \
    helper.get_timeStamp_and_compute_date_diff(test, date1, date2, dateDiff)

if binaryClass is True:
    train["binaryStatus"] = pd.DataFrame(np.zeros(train.shape[0]))
    train["binaryStatus"][train["OpenStatus"] == "open"] = 1

    test["binaryStatus"] = pd.DataFrame(np.zeros(test.shape[0]))
    test["binaryStatus"][test["OpenStatus"] == "open"] = 1

# it does not matter how the population of the training set look like
# for a random forest but it is good to examine it
f = open(output_file, 'w')
f.write("----------training data percent breakdown ----------\n")
helper.question_percent_breakdown(train, status, f)
f.write("Number of training obs = {0}\n".format(train.shape[0]))
f.write("----------test data percent breakdown ----------\n")
f.write("Number of testing obs = {0}\n".format(test.shape[0]))
helper.question_percent_breakdown(test, status, f)
f.write("------------------------------------------------\n")
f.write("--------input params----------------------------\n")
f.write("criterion for split = {0}\n".format(criterion))
f.write("max_features to be used for split = {0}\n".format(max_features))
f.write("binary classification or not = {0}\n".format(binaryClass))

# ------ initialize my random forest--------------------------------------
# some of the following input parameters for the RF might be ridiculous
# I don't know how many trees to use so I try to build many
n_estimators = int(train.shape[0] / 5e2)
f.write("no of tress = {0}\n".format(n_estimators))
f.write("------------------------------------------------\n")
print "No. of trees to be built = {0}\n".format(n_estimators)


myForest = \
    RandomForestClassifier(n_estimators=n_estimators,
                           criterion=criterion,
                           max_features=max_features,  # features = variables
                           oob_score=True,
                           n_jobs=4,
                           verbose=1)

# ------data to be used for building the tree----------------
# subset the training dataframe so that only specified variables
# get passed as input for building the forest
X = train[var]
y = train["binaryStatus"]
# the random forest algorithm only likes integer that indicate categories
#y = train["OpenStatus"].apply(hash)
forest = myForest.fit(X, y)

#--------prediction time-------------------------------------
test["RFclass"] = pd.DataFrame(forest.predict(test[var]))

#-------performance statistics ------------------------------
# compute if the prediction is correct or not
# if the two predicted class, the corresponding entry of "result" would be 1
if binaryClass is True:
    test["result"] = \
        pd.DataFrame(test["RFclass"] == test["binaryStatus"])
else:
    test["result"] = \
        pd.DataFrame(test["RFclass"] == test["OpenStatus"].apply(hash))

#overallPCC = np.sum(test["result"]) / test.shape[0] * 100
#
## PCC for different status
#allstatus = status + ["open"]
#PCC = []
#for status in allstatus:
#    if binaryClass is not True:
#        mask = test["OpenStatus"] == status
#    else:
#        mask = test["binaryStatus"] == helper.binaryStatusOrNot(status)
#    PCC.append(np.sum(test[mask]["result"]) / test[mask].shape[0] * 100)

#-------------write out results -----------------------------
f.write("OOB score : {0}\n".format(forest.oob_score_))
f.write("Features summary :\n")
f.write("{0}\n".format(var))
f.write("{0}\n".format(forest.feature_importances_))
f.write()
f.write("mean accuracy : {0}\n".format(forest.score(test[var],
                                                    test['binaryStatus'])))
#f.write("Overall PCC : {0}%\n".format(overallPCC))
#for i in range(len(allstatus)):
#    f.write(allstatus[i] + " PCC : {0}%\n".format(PCC[i]))
f.close()
