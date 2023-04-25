# import requests
# import re
# from collections import Counter
# import matplotlib.pyplot as plt

# # GitHub API endpoint for appium repository's commits
# url = "https://api.github.com/repos/SeleniumHQ/selenium "

# # Get the 100 most recent commits
# params = {'per_page': 100}
# response = requests.get(url, params=params)
# commits = response.json()

# # Extract commit messages and split them into words
# commit_messages = [commit['commit']['message'] for commit in commits]
# words = [re.findall(r'\w+', message) for message in commit_messages]

# # Count the number of words in each commit message
# word_counts = [len(words) for words in words]

# # Create a histogram of word counts
# word_count_freq = Counter(word_counts)
# plt.bar(word_count_freq.keys(), word_count_freq.values())
# plt.xlabel('Number of words')
# plt.ylabel('Frequency')
# plt.title('Histogram of Selenium Commit Message Word Counts')
# plt.show()
# import requests

# # Appiumのリポジトリのコミットメッセージを取得
# url = "https://api.github.com/repos/appium/appium/commits?per_page=100"
# response = requests.get(url)
# commits = response.json()

# # コミットメッセージの語数を数えてヒストグラムを作成
# histogram = [0, 0, 0 , 0, 0 , 0 , 0] # 0, 1, 2のバケット
# for commit in commits:
#     message = commit["commit"]["message"]
#     words = message.split()
#     word_count = len(words)
#     bucket_index = (word_count % 3) - 1
#     histogram[bucket_index] += 1

# # ヒストグラムを表示
# for i, count in enumerate(histogram):
#     lower_bound = i * 3
#     upper_bound = lower_bound + 2
#     print(f"{lower_bound}-{upper_bound}: {count}")

# import requests
# import re
import matplotlib.pyplot as plt

# # SeleniumのGitHubリポジトリAPIのURL
# url = 'https://api.github.com/repos/SeleniumHQ/selenium/commits'

# # APIから最新の1000件のコミット情報を取得
# response = requests.get(url + '?per_page=1000')
# commits = response.json()

# # 各コミットメッセージの語数を数える
# word_counts = []
# for commit in commits:
#     message = commit['commit']['message']
#     # コミットメッセージから改行や空白を取り除く
#     message = message.replace('\n', ' ').replace('\r', '')
#     message = re.sub(' +', ' ', message)
#     # 語数を数える
#     word_count = len(message.split(' '))
#     word_counts.append(word_count)

# # ヒストグラムを作成
# plt.hist(word_counts, bins=30, range=(0, 150))
# plt.xlabel('Word Count')
# plt.ylabel('Frequency')
# plt.title('Histogram of Word Count in Selenium Commit Messages')
# plt.show()
with open('commit_log3.txt', 'r') as f:
    line_lengths = [len(line.strip()) for line in f]

plt.hist(line_lengths, bins=20,range=(0, 200))
plt.xlabel('Length of lines')
plt.ylabel('Frequency')
plt.title('Histogram of line lengths')
plt.show()