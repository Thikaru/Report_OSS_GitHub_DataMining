import pandas as pd
import csv

# CSVファイルを二値化する時に欠損データの欄には，-1を入力している
# そのため，エクセルの表から-1のデータが一つでもある行を削除するプログラム
DataCleaning_CSV = "LastCSV/cleaning_data_-1.csv"
WriteFile_CSV = "LastCSV/cleaning_data_pickup.csv"


# CSVファイルを読み込む
df = pd.read_csv(DataCleaning_CSV)

# -1のセルが含まれる行を削除する
df = df[~(df == -1).any(axis=1)]

# 編集結果を新しいCSVファイルに書き込む
df.to_csv(WriteFile_CSV, index=False)
