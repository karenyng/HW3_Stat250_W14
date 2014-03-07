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

#-----initialize values------------------------------------------------
train_file = "../data/train-sample.csv"
test_file = "../data/train.csv"
date1 = "OwnerCreationDate"
date2 = "PostCreationDate"
dateDiff = "postOwnerTimeDiff"
# initialize list of strings of variables to be used for RF
var = [dateDiff,
       "ReputationAtPostCreation",
       "OwnerUndeletedAnswerCountAtPostTime",
       "OwnerUserId"]
reasons = \
    ["not constructive", "off topic", "not a real question", "too localized"]
#----------------------------------------------------------------------
train = pd.read_csv(train_file)
test = pd.read_csv()
train = \
    helper.get_timeStamp_and_compute_date_diff(train, date1, date2, dateDiff)

train["binaryStatus"] = pd.DataFrame(np.zeros(train.shape[0]))
train["binaryStatus"][train["OpenStatus"] == "open"] = 1

# it does not matter how the population of the training set look like
# for a random forest but it is good to examine it
helper.question_percent_breakdown(train, reasons)

# initialize my random forest
# some of the following input parameters for the RF are pretty ridiculous
n_estimators = int(train.shape[0] / 1e3)
print "No. of trees to be built = {0}".format(n_estimators)

myForest = \
    RandomForestClassifier(n_estimators=n_estimators,
                           criterion='gini',
                           max_features="sqrt",  # features = variables
                           bootstrap=True,
                           oob_score=True,
                           n_jobs=3,
                           verbose=1)

# data to be used for building the tree
X = train[var]
y = train["binaryStatus"]
forest = myForest.fit(X, y)
print "The score is {0}".format(forest.score(X,y))
print "The feature importance is {0}".format(forest.feature_importances_)
