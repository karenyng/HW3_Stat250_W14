import matplotlib.pyplot as plt


def plot_mean_median(var, reasons, df):
    """
    var = string
        denotes pandas dataframe column name
    allreasons = list of strings
        each string denotes the reason for closing the post
    df = pandas dataframe
    """
    allreasons = reasons + ["open"]
    Median = \
        [df[df["OpenStatus"] == reason][var].median() for reason in allreasons]
    mean = \
        [df[df["OpenStatus"] == reason][var].mean() for reason in allreasons]

    plt.plot(Median[0:4], range(4), 'ro', alpha=0.5, ms=6,
             label='closed median')
    plt.plot(mean[0:4], range(4), 'ro', alpha=0.8, ms=6, label='closed mean')
    plt.plot(Median[4], 4.0, 'bo', alpha=0.5, ms=6, label='open median')
    plt.plot(mean[4], 4.0, 'bo', alpha=0.8, ms=6, label='open mean')

    plt.yticks(range(len(allreasons)), allreasons, size=14)
    plt.ylim(-1, len(allreasons))
    xmin, xmax = plt.xlim()
    plt.xlim(xmin, xmax * 1.1)
    plt.xticks(size=14)
    plt.legend(loc='best', fontsize=10)
    plt.xlabel(var, size=16)
