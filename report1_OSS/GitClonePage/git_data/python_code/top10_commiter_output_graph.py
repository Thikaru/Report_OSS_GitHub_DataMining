import subprocess
import pandas as pd
import matplotlib.pyplot as plt

### ============ ###
# GitHubコミット作成者「Terraform」
### ============ ###
# gitコマンドを実行し、結果をバイト文字列として取得
output = subprocess.check_output(
    ['git', 'shortlog', '-s', '-n'], cwd='../../terraform',)
# バイト文字列を文字列に変換
output = output.decode('utf-8')
# 改行文字で分割してリストにする
lines = output.split('\n')

# コミット作成者のコミット数のCSVを作成
file_terraform = open(
    '../csv/commiter_info/creator_commit_num_terraform.csv', 'w')
file_terraform.write("author, commit_count\n")

commiter_commit_rank = []
x_data = []
y_data = []
for line in lines:
    tmp = line.split('\t')
    if len(tmp) >= 2:
        file_terraform.write(tmp[1]+','+str(int(tmp[0]))+'\n')
        x_data.append(tmp[1])
        y_data.append(int(tmp[0]))
file_terraform.close()

# 最初の10行を取得
x_data = x_data[:10]
y_data = y_data[:10]

fig = plt.figure(figsize=(6, 12), facecolor='lightblue')
plt.bar(x_data, y_data)

# グラフのタイトルや軸ラベルを設定
plt.title('Top 10 Commiters by Commit Count[Terraform]')
plt.xlabel('Author')
plt.ylabel('Commit Count')

# X軸のラベルを90度回転して表示
plt.xticks(rotation=30)

plt.savefig("../../figure/commiter_info/Top10_Commit_terraform.png")


### ============ ###
# GitHubコミット作成者「Vagrant」
### ============ ###
# gitコマンドを実行し、結果をバイト文字列として取得
output = subprocess.check_output(
    ['git', 'shortlog', '-s', '-n'], cwd='../../vagrant',)
# バイト文字列を文字列に変換
output = output.decode('utf-8')
# 改行文字で分割してリストにする
lines = output.split('\n')

# コミット作成者のコミット数のCSVを作成
file_vagrant = open('../csv/commiter_info/creator_commit_num_vagrant.csv', 'w')
file_vagrant.write("author, commit_count\n")

commiter_commit_rank = []
x_data = []
y_data = []
for line in lines:
    tmp = line.split('\t')
    if len(tmp) >= 2:
        file_vagrant.write(tmp[1]+','+str(int(tmp[0]))+'\n')
        x_data.append(tmp[1])
        y_data.append(int(tmp[0]))
file_vagrant.close()

# 最初の10行を取得
x_data = x_data[:10]
y_data = y_data[:10]

fig = plt.figure(figsize=(6, 12), facecolor='lightblue')
plt.bar(x_data, y_data)

# グラフのタイトルや軸ラベルを設定
plt.title('Top 10 Commiters by Commit Count[Vagrant]')
plt.xlabel('Author')
plt.ylabel('Commit Count')

# X軸のラベルを90度回転して表示
plt.xticks(rotation=30)

plt.savefig("../../figure/commiter_info/Top10_Commit_vagrant.png")
