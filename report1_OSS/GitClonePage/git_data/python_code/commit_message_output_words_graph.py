import subprocess
import numpy as np
import matplotlib.pyplot as plt

### ========== ###
# GitHubコミットメッセージカウント「Vagrant」
### ========== ###
# Git cloneする
# subprocess.run(['git', 'clone', 'https://github.com/hashicorp/vagrant'])

# Git logコマンドでコミットログを取得する
vagrant_result = subprocess.run(['git', 'log', '--oneline'],
                                cwd='../../vagrant', stdout=subprocess.PIPE)

# コミットメッセージとコミットをCSVファイルに保存する
commit_file_pointer = open(
    "../csv/commit_message/Vagrant_Commit_message_num.csv", "w")
commit_detail_file_pointer = open(
    "../text/commit_message/Vagrant_Commit_message_MaxMin.txt", "w")

commit_file_pointer.write("words,commit_message\n")
# 各コミットメッセージの文字の長さを計算する
commit_messages = vagrant_result.stdout.decode().split('\n')
message_lengths = [len(message.split(' ', 1)[1])
                   for message in commit_messages if message]
commit_count = 0  # コミットの個数をカウントする変数
commit_words_sum = 0
max = -10  # コミットメッセージの最大文字を求める
min = 100000  # コミットメッセージの最小文字数を求める
for line in message_lengths:
    commit_file_pointer.write(
        str(line)+','+commit_messages[commit_count] + '\n')
    commit_words_sum += line
    commit_count += 1
    if line > max:
        max = line

    if line < min:
        min = line
    # print(line)

commit_file_pointer.close()

hist, bin_edges = np.histogram(message_lengths, bins=range(0, max+10, 10))


print("vagrant max : " + str(max))
print("vagrant min : " + str(min))
# 結果の表示
for i, count in enumerate(hist):
    commit_detail_file_pointer.write(
        f"{bin_edges[i]} ~ {bin_edges[i+1]}: {count}" + '\n')
commit_detail_file_pointer.write("コミットメッセージ文字数最大：" + str(max) + '\n')
commit_detail_file_pointer.write("コミットメッセージ文字最小数：" + str(min) + '\n')
commit_detail_file_pointer.write("コミット数合計：" + str(commit_count) + '\n')
commit_detail_file_pointer.write(
    "コミット文字数平均：" + str(round(commit_words_sum/commit_count, 3)))

commit_detail_file_pointer.close()

# グラフのサイズを指定
fig = plt.figure(figsize=(18, 6), facecolor='lightblue')
# ヒストグラムの描画
plt.bar(bin_edges[:-1], hist, width=10, align='edge')

plt.xticks(np.arange(0, 420, 10))

for i in range(len(hist)):
    plt.text(bin_edges[i], hist[i], str(hist[i]),
             fontsize=10, ha='center', va='bottom')

# 軸ラベルの設定
plt.title('Commit Num Hist[Vagrant]')
plt.xlabel('Words')
plt.ylabel('Commit Num')

# グリッド線の表示
plt.grid(True)

# グラフの保存
plt.savefig("../../figure/commit_message/Commit_message_num_Vagrant.png")
# # グラフの表示
# plt.show()

### ========== ###
# GitHubコミットメッセージカウント「Vagrant」
### ========== ###
# Git cloneする
# subprocess.run(['git', 'clone', 'https://github.com/hashicorp/terraform'])

# Git logコマンドでコミットログを取得する
terraform_result = subprocess.run(['git', 'log', '--oneline'],
                                  cwd='../../terraform', stdout=subprocess.PIPE)

# コミットメッセージとコミットをCSVファイルに保存する
commit_file_pointer = open(
    "../csv/commit_message/Terraform_Commit_message_num.csv", "w")
commit_detail_file_pointer = open(
    "../text/commit_message/Terraform_Commit_message_MaxMin.txt", "w")

commit_file_pointer.write("words,commit_message\n")
# 各コミットメッセージの文字の長さを計算する
commit_messages = terraform_result.stdout.decode().split('\n')
message_lengths = [len(message.split(' ', 1)[1])
                   for message in commit_messages if message]
commit_words_sum = 0
commit_count = 0  # コミットの個数をカウントする変数
max = -10  # コミットメッセージの最大文字を求める
min = 100000  # コミットメッセージの最小文字数を求める
for line in message_lengths:
    commit_file_pointer.write(
        str(line)+','+commit_messages[commit_count] + '\n')
    commit_count += 1
    commit_words_sum += line
    if line > max:
        max = line

    if line < min:
        min = line
    # print(line)

commit_file_pointer.close()

hist, bin_edges = np.histogram(message_lengths, bins=range(0, max+10, 10))


print("terraform max : " + str(max))
print("terraform min : " + str(min))
# 結果の表示
for i, count in enumerate(hist):
    commit_detail_file_pointer.write(
        f"{bin_edges[i]} ~ {bin_edges[i+1]}: {count}" + '\n')
commit_detail_file_pointer.write("コミットメッセージ文字数最大：" + str(max) + '\n')
commit_detail_file_pointer.write("コミットメッセージ文字最小数：" + str(min) + '\n')
commit_detail_file_pointer.write("コミット数合計：" + str(commit_count) + '\n')
commit_detail_file_pointer.write(
    "コミット文字数平均：" + str(round(commit_words_sum/commit_count, 3)))

commit_detail_file_pointer.close()

# グラフのサイズを指定
fig = plt.figure(figsize=(18, 6), facecolor='lightblue')
# ヒストグラムの描画
plt.bar(bin_edges[:-1], hist, width=10, align='edge')

plt.xticks(np.arange(0, 420, 10))

for i in range(len(hist)):
    plt.text(bin_edges[i], hist[i], str(hist[i]),
             fontsize=10, ha='center', va='bottom')

# 軸ラベルの設定
plt.title('Commit Num Hist[Terraform]')
plt.xlabel('Words')
plt.ylabel('Commit Num')

# グリッド線の表示
plt.grid(True)

# グラフの保存
plt.savefig("../../figure/commit_message/Commit_message_num_Terraform.png")
# # グラフの表示
# plt.show()
