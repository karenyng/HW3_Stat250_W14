from markdown import markdown
import nltk
import numpy as np


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


def process_markdown(question):
    """ remove the markdown
    parameters
    ======
    question = ascii string of text mixed with markdown symbols

    returns
    ======
    cleaned = unicode string of pure text
    """
    html = markdown(question)
    cleaned = nltk.clean_html(html)
    cleaned = cleaned.translate({ord(u"\u2019"): ord(u"'")})
    return cleaned
