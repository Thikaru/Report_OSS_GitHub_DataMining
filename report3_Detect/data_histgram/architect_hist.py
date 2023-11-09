import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


# 元々あったCSVからアーキテクトのタイプごとの個数をカウントして
# 棒グラフを保存するプログラム
read_file = open('FakedataMonden_utf8_teacher_data.csv', "r")
rows = csv.reader(read_file)


# 主開発言語数ヒストグラム出力処理
# == START ==
# =========================#
# print(len(column_data))
test = {"": 0, "a: C/S": 0, "b: Web系": 0, "c: メインフレーム": 0, "d: スタンドアロン": 0}

for row in rows:
    for key in test.keys():
        if key == row[4]:
            test[key] += 1

x_values = list(test.keys())
y_values = list(test.values())

for i in range(len(x_values)):
    if x_values[i] == "":
        x_values[i] = "none"
    elif x_values[i] == "a: C/S":
        x_values[i] = "C/S"
    elif x_values[i] == "b: Web系":
        x_values[i] = "Web"
    elif x_values[i] == "c: メインフレーム":
        x_values[i] = "main frame"
    elif x_values[i] == "d: スタンドアロン":
        x_values[i] = "stand alone"

plt.bar(x_values, y_values, label="architect")

for i, v in enumerate(y_values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.xlabel('architect')
plt.ylabel('frequency')
plt.title('architect use')

plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()
plt.savefig('architect_teacher.png')
# 主開発言語数ヒストグラム出力処理
# == END ==
# =========================#
