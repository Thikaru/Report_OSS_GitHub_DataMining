import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


# 元々のCSVファイルから生産性を計算して，その生産性が閾値以下のものだけを残す．
# それ以外のデータは，今回の使用データの適用外とする．
# CSVファイルを受け取り　新しいCSVを作成する．
write_file = open('AllCSV/FakedataMonden_utf8_teacher_data_cleaning.csv', "w")
read_file = open('AllCSV/FakedataMonden_utf8_teacher_data.csv', "r")
rows = csv.reader(read_file)

efficent = []
i = 0
for row in rows:
    i = i+1
    if i == 1:
        write_file.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(
            row[5])+","+str(row[6])+","+str(row[7])+","+str(row[8])+","+str(row[9])+","+str(row[10])+"\n")
        continue
    if row[8] != "" and row[9] != "" and row[10] != "" and row[8] != 0 and row[9] != 0 and row[10] != 0:
        tmp = float(row[10])*float(row[8])
        if tmp != 0:
            tmp = float(row[9]) / tmp
            if tmp <= 20:
                write_file.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(
                    row[5])+","+str(row[6])+","+str(row[7])+","+str(row[8])+","+str(row[9])+","+str(row[10])+"\n")
            else:
                print(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(
                    row[5])+","+str(row[6])+","+str(row[7])+","+str(row[8])+","+str(row[9])+","+str(row[10])+"\n")
            efficent.append(tmp)

bin_width = 3
num_bins = int(np.ceil((max(efficent) - min(efficent)) / bin_width))

plt.hist(efficent, bins=num_bins, edgecolor='black')
plt.xlabel('range')
plt.ylabel('frequent')
plt.title('histgram')

plt.savefig('amount.png')
