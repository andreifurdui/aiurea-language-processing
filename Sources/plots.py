import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_mail_leaderboard(data):
    labels, y = zip(*data[:25])
    labels = np.asarray(labels)
    y = np.asarray(y)

    sns.set_style("whitegrid")
    p = sns.barplot(y=labels, x=y, palette=sns.cubehelix_palette(len(y), reverse=True))
    sns.despine(left=True, bottom=True)
    p.set_title("Mail Count")
    plt.show()


