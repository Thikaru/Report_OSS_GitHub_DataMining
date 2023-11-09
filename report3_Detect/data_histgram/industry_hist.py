import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


# 業種ごとの登場回数をカウントして
# 棒グラフとして画像を保存するプログラム
read_file = open('FakedataMonden_utf8_teacher_data.csv', "r")
rows = csv.reader(read_file)

# 業種ヒストグラム出力処理
# == START ==
# =========================#
industry_type = {"": 0, "a: 建設": 0, "b: 通信": 0, "c: 金融": 0, "d: 軍事": 0, "e: 小売": 0, "f: 製造": 0,
                 "g: 研究": 0, "h: その他": 0}

for row in rows:
    for key in industry_type.keys():
        if key == row[3]:
            industry_type[key] += 1

industry_x_values = list(industry_type.keys())
industry_y_values = list(industry_type.values())

for i in range(len(industry_x_values)):
    if industry_x_values[i] == "":
        industry_x_values[i] = "none"
    elif industry_x_values[i] == "h: その他":
        industry_x_values[i] = "others"
    elif industry_x_values[i] == "a: 建設":
        industry_x_values[i] = "construct"
    elif industry_x_values[i] == "b: 通信":
        industry_x_values[i] = "communication"
    elif industry_x_values[i] == "c: 金融":
        industry_x_values[i] = "finance"
    elif industry_x_values[i] == "d: 軍事":
        industry_x_values[i] = "military"
    elif industry_x_values[i] == "e: 小売":
        industry_x_values[i] = "retail"
    elif industry_x_values[i] == "f: 製造":
        industry_x_values[i] = "manufacture"
    elif industry_x_values[i] == "g: 研究":
        industry_x_values[i] = "research"


plt.bar(industry_x_values, industry_y_values, label="industry")
for i, v in enumerate(industry_y_values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.xlabel('Industry Type')
plt.ylabel('Frequency')
plt.title('Industry type use')

plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()
plt.savefig('industry_type_teacher.png')
# 業種ヒストグラム出力処理
# == END ==
# =========================#
