import pandas as pd
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# git log --pretty=format:"%cd" --date=short | uniq -c [日毎のコミットを取得するgit log コマンド]

### ============= ###
# 日毎のコミット数を折れ線グラフで表現「Terraform」
### ============= ###
result = subprocess.run(
    ["git", "log", "--pretty=format:\"%cd\"", "--date=short"], cwd='../../terraform', stdout=subprocess.PIPE)
# 出力を文字列に変換
output = result.stdout.decode("utf-8")
# 行ごとに分割し、日付でカウント
counts = {}
for line in output.strip().split("\n"):
    date = line.strip().replace('"', '')
    if date not in counts:
        counts[date] = 1
    else:
        counts[date] += 1

file_terraform = open(
    '../csv/commit_date/commit_num_per_date_terraform.csv', 'w')
file_sum_terraform = open(
    '../csv/commit_date/commit_num_per_date_sum_terraform.csv', 'w')
file_terraform.write("date,commit_count\n")
file_sum_terraform.write("date,commit_sum_count\n")

sum_commit = 0
commit_date_data = []
# 結果を表示
for date, count in reversed(counts.items()):
    sum_commit += count
    commit_date_data.append([int(count), date])
    file_terraform.write(date+","+str(count) + '\n')
    file_sum_terraform.write(date+","+str(sum_commit) + '\n')

df = pd.DataFrame(commit_date_data, columns=['commits', 'date'])

# 日時データをdatetime型に変換
df['date'] = pd.to_datetime(df['date'])

# 日ごとの累計コミット数を計算
df['cum_commits'] = df['commits'].cumsum()

# グラフを作成
fig, ax = plt.subplots(figsize=(10, 7))  # figsizeで表の大きさを指定
ax.plot(df['date'], df['cum_commits'])
ax.grid(color='grey', linestyle='--', linewidth=0.5)  # グリッド線を灰色に設定
# ax.set_facecolor('lightblue')  # 背景色を白色に設定

# グラフ外の背景色を黒色に設定
fig.patch.set_facecolor('lightblue')

# 年ごとに縦線を引く
years = pd.Series(df['date'].dt.year.unique())
for year in years:
    ax.axvline(pd.Timestamp(f'{year}-01-01'),
               color='grey', linestyle='--', linewidth=0.5)

# x軸に年の部分だけを表示
years = pd.Series(df['date'].dt.year.unique())
ax.set_xticks([pd.Timestamp(f'{year}-01-01') for year in years])
ax.set_xticklabels(years)

# グラフのタイトルと軸ラベルを設定
ax.set_title('Daily Cumulative Commits[Terraform]')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Commits')

# X軸のラベルを90度回転して表示
plt.xticks(rotation=30)

# グラフの保存
plt.savefig("../../figure/commit_date/Commit_num_date_terraform.png")
# # グラフを表示
# plt.show()


### ============= ###
# 日毎のコミット数を折れ線グラフで表現「Vagrant」
### ============= ###
result = subprocess.run(
    ["git", "log", "--pretty=format:\"%cd\"", "--date=short"], cwd='../../vagrant', stdout=subprocess.PIPE)
# 出力を文字列に変換
output = result.stdout.decode("utf-8")
# 行ごとに分割し、日付でカウント
counts = {}
for line in output.strip().split("\n"):
    date = line.strip().replace('"', '')
    if date not in counts:
        counts[date] = 1
    else:
        counts[date] += 1

file_vagrant = open(
    '../csv/commit_date/commit_num_per_date_vagrant.csv', 'w')
file_sum_vagrant = open(
    '../csv/commit_date/commit_num_per_date_sum_vagrant.csv', 'w')
file_vagrant.write("date,commit_count\n")
file_sum_vagrant.write("date,commit_sum_count\n")

sum_commit = 0
commit_date_data = []
# 結果を表示
for date, count in reversed(counts.items()):
    sum_commit += count
    commit_date_data.append([int(count), date])
    file_vagrant.write(date+","+str(count) + '\n')
    file_sum_vagrant.write(date+","+str(sum_commit) + '\n')

df = pd.DataFrame(commit_date_data, columns=['commits', 'date'])

# 日時データをdatetime型に変換
df['date'] = pd.to_datetime(df['date'])

# 日ごとの累計コミット数を計算
df['cum_commits'] = df['commits'].cumsum()

# グラフを作成
fig, ax = plt.subplots(figsize=(10, 7))
ax.plot(df['date'], df['cum_commits'])
ax.grid(color='grey', linestyle='--', linewidth=0.5)  # グリッド線を灰色に設定
# ax.set_facecolor('lightblue')  # 背景色を白色に設定

# グラフ外の背景色を黒色に設定
fig.patch.set_facecolor('lightblue')

# 年ごとに縦線を引く
years = pd.Series(df['date'].dt.year.unique())
for year in years:
    ax.axvline(pd.Timestamp(f'{year}-01-01'),
               color='grey', linestyle='--', linewidth=0.5)

# x軸に年の部分だけを表示
years = pd.Series(df['date'].dt.year.unique())
ax.set_xticks([pd.Timestamp(f'{year}-01-01') for year in years])
ax.set_xticklabels(years)

# グラフのタイトルと軸ラベルを設定
ax.set_title('Daily Cumulative Commits[Vagrant]')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Commits')

# X軸のラベルを90度回転して表示
plt.xticks(rotation=30)

# グラフの保存
plt.savefig("../../figure/commit_date/Commit_num_date_vagrant.png")
# # グラフを表示
# plt.show()
