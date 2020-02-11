import networkx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


def probability_distribution(data, bins_interval=1, margin=1):
    bins = range(min(data), max(data) + bins_interval - 1, bins_interval)
    print(len(bins))
    for i in range(0, len(bins)):
        print(bins[i])
    plt.xlim(min(data) - margin, max(data) + margin)
    plt.title("Probability-distribution")
    plt.xlabel('Interval')
    plt.ylabel('Probability')
    # 频率分布normed=True，频次分布normed=False
    prob, left, rectangle = plt.hist(x=data, bins=bins, normed=True, histtype='bar', color=['b'])
    for x, y in zip(left, prob):
        # 字体上边文字
        # 频率分布数据 normed=True
        plt.text(x + bins_interval / 2, y + 0.003, '%.2f' % y, ha='center', va='top')
        # 频次分布数据 normed=False
        # plt.text(x + bins_interval / 2, y + 0.25, '%.2f' % y, ha='center', va='top')
    plt.show()

date_num = []
with open("./datasets/wikivote_new.txt","r") as f:
    lines = f.readlines()
    nlink = len(lines)
    for i in range(nlink):
        line = lines[i].strip('\n').split()
        date = line[4].split('-')
        date_num.append(int((int(date[0])-2004)*12+int(date[1])))
    probability_distribution(data=date_num, bins_interval=1, margin=1)


