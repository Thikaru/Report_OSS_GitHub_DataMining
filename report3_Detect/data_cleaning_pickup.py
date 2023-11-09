import pandas as pd
import csv

# 変数選択を行い，残したい変数を二値化する処理などを行うプログラム


# 読み込むCSVファイル：データクリーニングしたいCSV
DataCleaning_CSV = "FakedataMonden_utf8_test_data.csv"
# 書き込むCSVファイル名：データクリーニングしたCSV
WriteFile_CSV = "cleaning_data_test_-1.csv"

# どのカラムに対して処理を行うかどうか
# 行うカラムは，data_histgramなどで分析した結果を選択
is_development_type = True
is_industry_type = True
is_architect_type = True
is_programing_type = True
is_request_type = True


def development_type():
    global body_record
    if row[2] == "a: 新規開発":
        body_record = body_record + ",1"
        return True
    elif row[2] == "b: 改修・保守":
        body_record = body_record + ",0"
        return True
    elif row[2] == "c: 再開発":
        body_record = body_record + ",0"
        return True
    else:
        body_record = body_record + ",-1"
        return False


def industry_type():
    global body_record
    if row[3] == "a: 建設":
        body_record = body_record + ",0,0,0"
        return True
    elif row[3] == "b: 通信":
        body_record = body_record + ",0,0,1"
        return True
    elif row[3] == "c: 金融":
        body_record = body_record + ",0,1,0"
        return True
    elif row[3] == "d: 軍事":
        body_record = body_record + ",0,0,0"
        return True
    elif row[3] == "e: 小売":
        body_record = body_record + ",0,0,0"
        return True
    elif row[3] == "f: 製造":
        body_record = body_record + ",1,0,0"
        return True
    elif row[3] == "g: 研究":
        body_record = body_record + ",0,0,0"
        return True
    elif row[3] == "h: その他":
        body_record = body_record + ",0,0,0"
        return True
    else:
        body_record = body_record + ",-1,-1,-1"
        return False


def architect_type():
    global body_record
    if row[4] == "a: C/S":
        body_record = body_record + ",0"
        return True
    elif row[4] == "b: Web系":
        body_record = body_record + ",1"
        return True
    elif row[4] == "c: メインフレーム":
        body_record = body_record + ",0"
        return True
    elif row[4] == "d: スタンドアロン":
        body_record = body_record + ",0"
        return True
    else:
        body_record = body_record + ",-1"
        return False


def programing_type():
    global body_record
    if row[5] == "ASP":
        body_record = body_record + ",0,0,1"
        return True
    elif row[5] == "ASP.NET":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "C":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "C++":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "C#":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "COBOL":
        body_record = body_record + ",0,1,0"
        return True
    elif row[5] == "Java":
        body_record = body_record + ",1,0,0"
        return True
    elif row[5] == "PHP":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "PL/I":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "SQL":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "VB":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "VB.NET":
        body_record = body_record + ",0,0,0"
        return True
    elif row[5] == "その他":
        body_record = body_record + ",0,0,0"
        return True
    else:
        body_record = body_record + ",-1,-1,-1"
        return False


def request_type():
    global body_record
    if row[6] == "a：非常に明確":
        body_record = body_record + ",1"
        return True
    elif row[6] == "b：かなり明確":
        body_record = body_record + ",1"
        return True
    elif row[6] == "c：ややあいまい":
        body_record = body_record + ",0"
        return True
    elif row[6] == "d：非常にあいまい":
        body_record = body_record + ",0"
        return True
    else:
        body_record = body_record + ",-1"
        return False


## ================= ##
##   main処理　START  ##
## ================= ##
read_file = open(DataCleaning_CSV, "r")
rows = csv.reader(read_file)

header = "ID,year,dev-type:new,arc-type:web,lang:Java,lang:COBOL,lang:ASP,ind-type:manufacture,ind-type:finance,ind-type:comm,req:clear,PM,FP,range-dev,month,man-month\n"
body_record = ""

write_file = open(WriteFile_CSV, "w")

write_file.write(header)

i = 0
for row in rows:
    i = i+1
    if i == 1:
        continue
    body_record = ''
    body_record = body_record + str(i)

    body_record = body_record + "," + row[1]

    if is_development_type == True:
        development_type()
    if is_architect_type ==True:
        architect_type()
    if is_programing_type == True:
        programing_type()
    if is_industry_type == True:
        industry_type()
    if is_request_type == True:
        request_type()

    if row[7] != '':
        body_record = body_record + "," + row[7]
    else:
        body_record = body_record + ",-1"

    if row[9] != '':
        body_record = body_record + "," + row[9]
    else:
        body_record = body_record + ",-1"

    if row[8] != '':
        body_record = body_record + "," + row[8]
    else:
        body_record = body_record + ",-1"

    if row[10] != '':
        body_record = body_record + "," + row[10]
    else:
        body_record = body_record + ",-1"

    if row[8] != '' and row[10] != '':
        tmp = int(row[8])*int(row[10])
        body_record = body_record + ","+str(tmp)
    else:
        body_record = body_record + ",-1"

    body_record = body_record + '\n'
    write_file.write(body_record)

read_file.close()
## ================= ##
##   main処理　END    ##
## ================= ##


# def development_type():
#     global body_record
#     if row[2] == "a: 新規開発":
#         body_record = body_record + "1,0"
#         return True
#     elif row[2] == "b: 改修・保守":
#         body_record = body_record + "0,1"
#         return True
#     elif row[2] == "c: 再開発":
#         body_record = body_record + "0,0"
#         return True
#     else:
#         body_record = body_record + "-1,-1"
#         return False


# def industry_type():
#     global body_record
#     if row[2] == "a: 建設":
#         body_record = body_record + "1,0,0,0,0,0,0"
#         return True
#     elif row[2] == "b: 通信":
#         body_record = body_record + "0,1,0,0,0,0,0"
#         return True
#     elif row[2] == "c: 金融":
#         body_record = body_record + "0,0,1,0,0,0,0"
#         return True
#     elif row[2] == "d: 軍事":
#         body_record = body_record + "0,0,0,1,0,0,0"
#         return True
#     elif row[2] == "e: 小売":
#         body_record = body_record + "0,0,0,0,1,0,0"
#         return True
#     elif row[2] == "f: 製造":
#         body_record = body_record + "0,0,0,0,0,1,0"
#         return True
#     elif row[2] == "g: 研究":
#         body_record = body_record + "0,0,0,0,0,0,1"
#         return True
#     elif row[2] == "h: その他":
#         body_record = body_record + "0,0,0,0,0,0,0"
#         return True
#     else:
#         body_record = body_record + "-1,-1,-1,-1,-1,-1,-1"
#         return False


# def architect_type():
#     global body_record
#     print("TEST")


# def request_type():
#     global body_record
#     if row[2] == "a：非常に明確":
#         body_record = body_record + "1,0,0"
#         return True
#     elif row[2] == "b：かなり明確":
#         body_record = body_record + "0,1,0"
#         return True
#     elif row[2] == "c：ややあいまい":
#         body_record = body_record + "0,0,1"
#         return True
#     elif row[2] == "d：非常にあいまい":
#         body_record = body_record + "0,0,0"
#         return True
#     else:
#         body_record = body_record + "-1,-1,-1"
#         return False
