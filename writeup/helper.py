from __future__ import division
from markdown import markdown
import nltk
import numpy as np
import pandas as pd


def print_question(closed, row, reason, contentCol):
    """ quickly summarizes the body of the question
    closed = pandas data frame
    row = integer
    reason = integer, index to reasons
    reasons = list of strings
    contentCol = list of strings
        expects format as
        [u'Title', u'BodyMarkdown', u'Tag1', u'Tag2', u'Tag3', u'Tag4',
        u'Tag5']
        denoting the column names for contents
    """
    print reason
    print "-----------------------------------------------------------------"
    print closed[closed["OpenStatus"] == reason][contentCol[0]].iloc[row]
    print "-----------------------------------------------------------------"
    print closed[closed["OpenStatus"] == reason][contentCol[1]].iloc[row]
    print "-----------------------------------------------------------------"
    tags = [closed[closed["OpenStatus"] == reason][contentCol[i]].iloc[row]
            for i in range(2, 7)]
    for tag in tags:
        if type(tag) == unicode and tag != "NaN":
            print "Tag : {0}".format(tag)
        elif type(tag) == float and ~np.isnan(tag):
            print "Tag : {0}".format(tag)


def detect_code_from_html(df, code_word_num):
    """ this should grab the <pre> and <code> tags and analyze the code in
    between
    """

    return df


def process_markdown(question):
    """ remove the markdown
    parameters
    ======
    question = ascii string of text mixed with markdown symbols

    returns
    ======
    cleaned = unicode string of pure text
    """
    question = str.decode(question, 'utf-8')
    html = markdown(question)
    cleaned = nltk.clean_html(html)
    # ad hoc solution for removing apostrophe
    cleaned = cleaned.translate({ord(u"\u2019"): ord(u"'")})
    return cleaned


def get_timeStamp_and_compute_date_diff(df, date1, date2, dateDiff):
    """ computes and returns date2 - date1 in days
    Parameters
    ==========
    df = pandas dataframe
    date1 = string
        contains the column name of dates in format of strings
    date2 = string
        contains the column name of dates in format of strings
    dateDiff = string
        the column name containing results to be added to the df

    Returns
    =======
    Altered df date1 and date2 column are now in format of timestamp
    and a new column dateDiff
    """
    df[date2] = df[date2].apply(pd.Timestamp)
    df[date1] = df[date1].apply(pd.Timestamp)
    df[dateDiff] = df[date2] - df[date1]
    df[dateDiff] = df[dateDiff].apply(float)
    df[dateDiff] = np.round(np.abs(df[dateDiff] / 1e9 / 60. / 60. / 24.))

    return df


def num_of_stop_words():
    return


def question_percent_breakdown(df, reasons, f=None):
    """print the percentage breakdown of the df
    df = pandas dataframe
    reasons = list of strings
    """
    total = df.shape[0]
    print "-----------------------------------------------------------"
    print "Closed percent: " + \
        " {0}%".format(df[df["OpenStatus"] != "open"].shape[0] / total *
                       100)

    for reason in reasons:
        print reason + " percent: " + \
            " {0}%".format(df[df["OpenStatus"] == reason].shape[0] /
                           total * 100)
    print "-----------------------------------------------------------\n"
    if f is not None:
        f.write("Closed percent: " +
                " {0}%".format(df[df["OpenStatus"] != "open"].shape[0] /
                               total * 100) + "\n")

        for reason in reasons:
            f.write(reason + " percent: " +
                    " {0}%".format(df[df["OpenStatus"] == reason].shape[0] /
                                   total * 100) + "\n")


def binaryStatusOrNot(status):
    if status == "open":
        return 1
    else:
        return 0
    return
