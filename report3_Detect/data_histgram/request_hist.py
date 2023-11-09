import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


# 要求仕様の明確度ごとの登場回数をカウントして
# 棒グラフとして画像を保存するプログラム
read_file = open('FakedataMonden_utf8_teacher_data.csv', "r")
rows = csv.reader(read_file)


# 主開発言語数ヒストグラム出力処理
# == START ==
# =========================#
# print(len(column_data))
test = {"": 0, "a：非常に明確": 0, "b：かなり明確": 0, "c：ややあいまい": 0, "d：非常にあいまい": 0}

for row in rows:
    for key in test.keys():
        if key == row[6]:
            test[key] += 1

x_values = list(test.keys())
y_values = list(test.values())

for i in range(len(x_values)):
    if x_values[i] == "":
        x_values[i] = "none"
    elif x_values[i] == "a：非常に明確":
        x_values[i] = "clear"
    elif x_values[i] == "b：かなり明確":
        x_values[i] = "soft clear"
    elif x_values[i] == "c：ややあいまい":
        x_values[i] = "ambiguous"
    elif x_values[i] == "d：非常にあいまい":
        x_values[i] = "hard ambiguous"

plt.bar(x_values, y_values, label="request")

for i, v in enumerate(y_values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.xlabel('request')
plt.ylabel('frequency')
plt.title('request use')

plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()
plt.savefig('request_teacher.png')
# 主開発言語数ヒストグラム出力処理
# == END ==
# =========================#
