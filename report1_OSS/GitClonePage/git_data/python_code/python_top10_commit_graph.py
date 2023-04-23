import subprocess
import pandas as pd
import matplotlib.pyplot as plt


### =============###
# Top10コミット[Terraform]
### =============###
# CSVファイルの読み込み[Terraform]
df = pd.read_csv('../csv/top10_terraform.csv',
                 header=None, names=['count', 'author'])

fig = plt.figure(figsize=(6, 12), facecolor='lightblue')
plt.bar(df['author'], df['count'])

# グラフのタイトルや軸ラベルを設定
plt.title('Top 10 Commiters by Commit Count[Terraform]')
plt.xlabel('Author')
plt.ylabel('Commit Count')

# X軸のラベルを90度回転して表示
plt.xticks(rotation=30)

plt.savefig("../../figure/Top10_Commit_terraform.png")
# グラフを表示
# plt.show()

### =============###
# Top10コミット[Vagrant]
### =============###
# CSVファイルの読み込み[Vargant]
df = pd.read_csv('../csv/top10_vagrant.csv',
                 header=None, names=['count', 'author'])

fig = plt.figure(figsize=(6, 12), facecolor='lightblue')
plt.bar(df['author'], df['count'])

# グラフのタイトルや軸ラベルを設定
plt.title('Top 10 Commiters by Commit Count[Vagrant]')
plt.xlabel('Author')
plt.ylabel('Commit Count')

# X軸のラベルを90度回転して表示
plt.xticks(rotation=30)

plt.savefig("../../figure/Top10_Commit_vagrant.png")
# グラフを表示
# plt.show()
