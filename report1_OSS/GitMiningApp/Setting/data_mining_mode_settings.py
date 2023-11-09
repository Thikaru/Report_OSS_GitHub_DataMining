###############################
#### ライブラリ類           #####
###############################
import json
import datetime
# pip install pytz
import pytz

# 共通して使用する変数
import Setting.common_settings as CommonSetting


###############################
#### 定数                 #####
###############################
CLIENT_ID = ""
CLIENT_SECRET = ""
USER_NAME = "Thikaru"

GIT_FIXED_URL = "https://api.github.com/repos/"


###############################
#### 変数                 #####
###############################
# TimeZone/日付 指定
jp = pytz.timezone('Asia/Tokyo')
# 集計終了日（= Today )
finish_date = datetime.datetime.now().astimezone(
    jp).replace(hour=0, minute=0, second=0, microsecond=0)
# 集計開始日（= 1日前）
start_date = finish_date - datetime.timedelta(1)


# query設定
git_client_id_prefix = "&client_id="
git_client_secret_prefix = "&client_secret="
git_client_id_query = "&client_id=" + CLIENT_ID
git_client_secrets_query = "&client_secret=" + CLIENT_SECRET

# vargrant : hashicorp/vagrant
# terraform : hashicorp/terraform
GIT_REPOSITORY = "hashicorp/vagrant/"
GIT_GET_INFO_PREFIX = "commits"
GIT_GET_ONE_REQUESTS = "100"

# 変数初期化
total_commit_count = 0  # 合計commit数
repo_url_page_num = 1  # repository取得の際のpagenation用

API_Link_Count = 10

file_path_csv = ''
