import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


# 開発種別ごとの登場回数をカウントして
# 棒グラフとして画像を保存するプログラム
read_file = open('FakedataMonden_utf8_teacher_data.csv', "r")
rows = csv.reader(read_file)


# 主開発言語数ヒストグラム出力処理
# == START ==
# =========================#
# print(len(column_data))
test = {"": 0, "a: 新規開発": 0, "b: 改修・保守": 0, "c: 再開発": 0}

for row in rows:
    for key in test.keys():
        if key == row[2]:
            test[key] += 1

x_values = list(test.keys())
y_values = list(test.values())

for i in range(len(x_values)):
    if x_values[i] == "":
        x_values[i] = "none"
    elif x_values[i] == "a: 新規開発":
        x_values[i] = "new"
    elif x_values[i] == "b: 改修・保守":
        x_values[i] = "continuous"
    elif x_values[i] == "c: 再開発":
        x_values[i] = "re-development"

plt.bar(x_values, y_values, label="development-type")

for i, v in enumerate(y_values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.xlabel('development-type')
plt.ylabel('frequency')
plt.title('development-type use')

plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()
plt.savefig('development-type_teacher.png')
# 主開発言語数ヒストグラム出力処理
# == END ==
# =========================#
