import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_bar_chart(data, title):
    labels, y = zip(*data[:25])
    labels = np.asarray(labels)
    y = np.asarray(y)

    sns.set_style("whitegrid")
    p = sns.barplot(y=labels, x=y, palette=sns.cubehelix_palette(len(y), start=2, rot=0, dark=0, light=.95, reverse=True))
    sns.despine(left=True, bottom=True)
    p.set_title(title)
    plt.show()

def plot_day_bar_chart(data):
    labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    sns.set_style("whitegrid")
    sns.barplot(x = labels, y = data, palette=sns.color_palette("pastel"))
    plt.show()

def plot_clock_histogram(data):
    sns.set_context('poster')
    sns.set_style('white')
    bottom = 2
    bins = 47
    theta = np.linspace(0.0, 2 * np.pi, bins, endpoint=False)
    radii, tick = np.histogram(data, bins=bins)
    print(radii)
    width = (2 * np.pi) / bins
    plt.figure(figsize=(12, 8))
    ax = plt.subplot(111, polar=True)
    bars = ax.bar(theta, radii, width=width, bottom=bottom)
    # set the lable go clockwise and start from the top
    ax.set_theta_zero_location("N")
    # clockwise
    ax.set_theta_direction(-1)

    # set the label
    ticks = ['0:00', '3:00', '6:00', '9:00', '12:00', '15:00', '18:00', '21:00']
    ax.set_xticklabels(ticks)

    plt.show()

def plot_time_density(data):
    for member in data:
        sns.distplot(data[member], hist=False, kde=True,
                     kde_kws={'shade': True, 'linewidth': 2},
                     label=member)

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Density')
    plt.xticks(np.arange(0, 24, 1))
    plt.show()