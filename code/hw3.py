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
#from sklearn.ensemble import RandomForestClassifier

# homebrewed module from path
sys.path.append('../writeup/')
import helper

#-----initialize values------------------------------
file = "../data/train-sample.csv"
date1 = "OwnerCreationDate"
date2 = "PostCreationDate"
dateDiff = "postOwnerTimeDiff"
# initialize list of strings of variables to be used for RF
var = [dateDiff,
       "ReputationAtPostCreation",
       "OwnerUndeletedAnswerCountAtPostTime"]

df = pd.read_csv(file, nrows=100)
df = helper.get_timeStamp_and_compute_date_diff(df, date1, date2, dateDiff)

# replace the markdown part in place by pure text
# maybe compute the amount of code in the process
df['BodyMarkdown'] = df['BodyMarkdown'].apply(helper.process_markdown)
df['BodyWordTokens'] = df['BodyMarkdown'].apply(nltk.word_tokenize)
df['BodyWordCount'] = df['BodyWordTokens'].apply(len)
df['BodyPOS'] = df['BodyWordTokens'].apply(nltk.pos_tag)

# there does not seem to be any markdown in the title
# directly compute word tokens and pos
df['Title'] = df['Title'].apply(nltk.word_tokenize)
TitlePOS = df['Title'].apply(nltk.pos_tag)
df['TitleKeywords'] = pd.DataFrame(nltk.stem(TitlePOS))
