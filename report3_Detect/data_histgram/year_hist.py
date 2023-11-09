import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


# 開発年後ごとの登場回数をカウントして
# 棒グラフとして画像を保存するプログラム
read_file = open('FakedataMonden_utf8_teacher_data.csv', "r")
rows = csv.reader(read_file)


# 主開発言語数ヒストグラム出力処理
# == START ==
# =========================#
# print(len(column_data))
test = {"": 0, "2004": 0, "2005": 0, "2006": 0, "2007": 0, "2008": 0, "2009": 0, "2010": 0,
        "2011": 0, "2012": 0, "2013": 0, "2014": 0}

for row in rows:
    for key in test.keys():
        if key == row[1]:
            test[key] += 1

x_values = list(test.keys())
y_values = list(test.values())

plt.bar(x_values, y_values, label="year")

for i, v in enumerate(y_values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.xlabel('year')
plt.ylabel('frequency')
plt.title('year use')

plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()
plt.savefig('year_teacher.png')
# 主開発言語数ヒストグラム出力処理
# == END ==
# =========================#
