#======================================================================
# Author: Karen Ng <karenyng@ucdavis.edu>
# Date: 03/16/2014
# Winter 14 Stat 250 HW 3
# "production" code for classifying SO questions
#======================================================================
from __future__ import division
import sys
import nltk
import pandas as pd
from sklearn import RandomForestClassifier

# homebrewed module from path
sys.path.append('../writeup/')
import helper

#-----initialize values------------------------------
file = "../data/train-sample.csv"
date1 = "OwnerCreationDate"
date2 = "PostCreationDate"
dateDiff = "postOwnerTimeDiff"
# initialize list of strings of variables to be used for RF
var = [dateDiff, "ReputationAtPostCreation",
       "OwnerUndeletedAnswerCountAtPostTime"]

df = pd.read_csv(file)
df = helper.get_timeStamp_and_compute_date_diff(df, date1, date2, dateDiff)

