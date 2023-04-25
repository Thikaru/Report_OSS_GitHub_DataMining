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
