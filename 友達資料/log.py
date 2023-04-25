import datetime
import numpy as np
import matplotlib.pyplot as plt

x = []
y = []

commit_count = {}
with open("commit_log.txt") as file:
    for line in file:
        date = datetime.datetime.strptime(line.strip(), "%Y-%m-%d")
        year = date.strftime("%Y")
        if year in commit_count:
            commit_count[year] += 1
        else:
            commit_count[year] = 1

for year in sorted(commit_count.keys()):
    print(year, commit_count[year])

y = [394,911,2013,741,946,1176,1985,3961,2671,1588,966,1229,1516,1851,1665,1254,1604,1597,1417,316]

plt.figure(figsize=(25, 5))
plt.plot(list(sorted(commit_count.keys())), y)
plt.xlabel("Date")
plt.ylabel("Commit Count")
plt.title("Commit History of Selenium")
plt.show()


# テキストファイルからデータを読み込む
with open('commit_log2.txt', 'r') as f:
    lines = f.readlines()

# データを整形して棒グラフを作成
authors = [line.split()[1] for line in lines]
counts = [int(line.split()[0]) for line in lines]

plt.bar(authors, counts)
plt.xticks(rotation=90)
plt.ylabel('Commit Count')
plt.show()

