###############################
#### ライブラリ類           #####
###############################
# 共通して使用する変数
import Setting.common_settings as CommonSetting


###############################
#### 定数                 #####
###############################
GIT = 'git'
CLONE = 'clone'
LOG = 'log'
GITHUB_CLONE_PREFIX = 'https://github.com/'

GITHUB_REPOSITORY = "GitHubCloneRepository/"

DATA_MINING_DIR_CSV = 'OutputMiningData/csv/'
DATA_MINING_DIR_TEXT = 'OutputMiningData/text/'
DATA_MINING_DIR_GRAPH = 'OutputMiningData/graph/'

CREATOR_COMMIT_NUM = 'commiter_info/'
COMMIT_PER_DATE = 'commit_date/'
COMMIT_MESSAGE_WORDS = 'commit_message/'

###############################
#### 変数                 #####
###############################
GitHub_Repository_creater = 'hashicorp'
GitHub_Repository_name = 'terraform'

# どのデータマイニングを行うのか決めるオプション
data_mining_menu_option = 0
data_mining_option = [
    "日毎のコミット数を累積棒グラフで出力する分析",
    "コミット数TOP10の棒グラフを分析",
    "コミットメッセージの文字数の分布を分析",
]

# 日毎のコミットデータ保存ファイル名
date_commit_csv = ''
date_commit_sum_csv = ''
date_commit_graph = ''
# TOP10コミット数保存ファイル名
commiter_csv = ''
commit_top10_graph = ''
# コミットメッセージ分布保存ファイル名
commit_message_csv = ''
commit_message_txt = ''
commit_message_graph = ''
