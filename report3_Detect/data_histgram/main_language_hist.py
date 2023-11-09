import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


# 主言語ごとの登場回数をカウントして
# 棒グラフとして画像を保存するプログラム
read_file = open('FakedataMonden_utf8_teacher_data.csv', "r")
rows = csv.reader(read_file)


# 主開発言語数ヒストグラム出力処理
# == START ==
# =========================#
# print(len(column_data))
test = {"": 0, "その他": 0, "ASP": 0, "ASP.NET": 0, "C": 0, "C＃": 0, "C++": 0,
        "COBOL": 0, "Java": 0, "PHP": 0, "PL/I": 0, "SQL": 0, "VB": 0, "VB.NET": 0}

for row in rows:
    for key in test.keys():
        if key == row[5]:
            test[key] += 1

x_values = list(test.keys())
y_values = list(test.values())

for i in range(len(x_values)):
    if x_values[i] == "":
        x_values[i] = "none"
    elif x_values[i] == "その他":
        x_values[i] = "other"
    elif x_values[i] == "C＃":
        x_values[i] = "C#"
    elif x_values[i] == "C＋＋":
        x_values[i] = "C++"

plt.bar(x_values, y_values, label="programing")

for i, v in enumerate(y_values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.xlabel('programing language')
plt.ylabel('frequency')
plt.title('programing language use')

plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()
plt.savefig('programing_language_teacher.png')
# 主開発言語数ヒストグラム出力処理
# == END ==
# =========================#
