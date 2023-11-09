###############################
#### ライブラリ類           #####
###############################
# GUIライブラリ
import PySimpleGUI as sg
import requests
import json
import datetime
# pip install pytz
import pytz

# 共通して使用する変数
import Setting.common_settings as CommonSetting
import Controller.common_controller as CommonController
# データマイニングモードないで使用する変数を読み込む
import Setting.data_mining_mode_settings as DataMiningModeSetting
# データマイニングモードのページレイアウトを読み込む
import Window.data_mining_mode_window as DataMiningModeWindow


######## ==================== ########
# イベントハンドラ処理
######## ==================== ########
def DataMiningModeEventHandler():
    if CommonSetting.Event == '-data-mining-setting-mode-':
        print("-data-mining-setting-mode-")
        if CommonSetting.Page_index == 12:
            CommonSetting.Error_message = ''
        DataMiningModeWindow.MakeDataMiningSettingDMMPage()
    elif CommonSetting.Event == '-execute-github-api-get-json-':
        print("-execute-github-api-get-json-")
        CheckGitHubAPIURLDetail()
    elif CommonSetting.Event == '':
        print("TEST")


######## ============== ########
# 入力された変数が，正しいものなのかを判定する
######## ============== ########
def CheckGitHubAPIURLDetail():
    if IsSetGitHubAPIURL() == True:
        CommonController.ResetErrorMessage()
        GitHubAPI_Commit_Data_To_JSON_File()
        DataMiningModeWindow.ResultGitHubDataMiningDMMPage()
    else:
        print("Error : 変数がうまく設定できていません!!")
        DataMiningModeWindow.MakeDataMiningSettingDMMPage()


######## ============== ########
# 入力された内容を変数に格納しながらエラーがある場合はFalseを返す
######## ============== ########
def IsSetGitHubAPIURL():
    # 空白でもOK
    DataMiningModeSetting.CLIENT_ID = CommonSetting.Value['-client-id-']
    # 空白でもOK
    DataMiningModeSetting.CLIENT_SECRET = CommonSetting.Value['-client-secret-']
    if CommonSetting.Value['-repository-detail-'] == '':
        CommonSetting.Error_message = "repository_user_name/repository_name/を入力してください"
        return False
    else:
        DataMiningModeSetting.GIT_REPOSITORY = CommonSetting.Value['-repository-detail-']

    if CommonSetting.Value['-repository-info-prefix-'] == '':
        CommonSetting.Error_message = "入手したい情報を入力してください[commits]"
        return False
    else:
        DataMiningModeSetting.GIT_GET_INFO_PREFIX = CommonSetting.Value[
            '-repository-info-prefix-']

    if CommonSetting.Value['-start_date-'] == '':
        CommonSetting.Error_message = "始まりの期間を入力してください"
        return False
    else:
        DataMiningModeSetting.start_date = CommonSetting.Value['-start_date-']

    if CommonSetting.Value['-end-date-'] == '':
        CommonSetting.Error_message = "終わりの期間を指定を入力してください"
        return False
    else:
        DataMiningModeSetting.finish_date = CommonSetting.Value['-end-date-']

    if CommonSetting.Value['-git-get-one-request-'] == '':
        CommonSetting.Error_message = "1通信あたりのコミット情報獲得数を入力してください「通常は100」"
        return False
    else:
        DataMiningModeSetting.GIT_GET_ONE_REQUESTS = int(
            CommonSetting.Value['-git-get-one-request-'])

    if CommonSetting.Value['-Api-link-count-'] == '':
        CommonSetting.Error_message = "API通信の制限を決めるは数字を入力してください．「5000以上で最大」"
        return False
    else:
        DataMiningModeSetting.API_Link_Count = int(
            CommonSetting.Value['-Api-link-count-'])

    if CommonSetting.Value['-input-data-preserve-csv-'] == '':
        CommonSetting.Error_message = "保存するファイル名を指定してください[.csv]"
        return False
    else:
        DataMiningModeSetting.file_path_csv = CommonSetting.Value['-input-data-preserve-csv-']
        print(CommonSetting.Value['-input-data-preserve-csv-'])

    print("ALL Variable True")
    return True


def WriteFileCSVHeader(file_pointer):
    file_pointer.write("commit_author,")
    file_pointer.write("commit_author_email,")
    file_pointer.write("commit_date,")
    file_pointer.write("commit_message,")
    file_pointer.write("commit_message_words,")
    file_pointer.write("commit_permittee,")
    file_pointer.write("commit_permittee_email,")
    file_pointer.write("commit_permission_date\n")


def WriteFileCSVGitHubData(file_pointer, commit):
    commit_datetime = datetime.datetime.fromisoformat(
        commit["commit"]["committer"]["date"].replace('Z', '+00:00')).astimezone(DataMiningModeSetting.jp)
    commit_author = commit["commit"]["author"]["name"] if commit["commit"]["author"]["name"] else ''
    commit_author_email = commit["commit"]["author"]["email"] if commit["commit"]["author"]["email"] else ''
    commit_date = commit["commit"]["author"]["date"] if commit["commit"]["author"]["date"] else ''
    commit_permittee = commit["commit"]["committer"]["name"] if commit["commit"]["committer"]["name"] else ''
    commit_permittee_email = commit["commit"]["committer"]["email"] if commit["commit"]["committer"]["email"] else ''
    allow_commit_date = commit["commit"]["committer"]["date"] if commit["commit"]["committer"]["date"] else ''
    commit_message = commit["commit"]["message"] if commit["commit"]["message"] else ''
    commit_message_words_num = len(
        commit_message) if len(commit_message) else 0
    file_pointer.write(commit_author+",")
    file_pointer.write(commit_author_email+",")
    file_pointer.write(commit_date+",")
    file_pointer.write(commit_message + ",")
    file_pointer.write(str(commit_message_words_num) + ',')
    file_pointer.write(commit_permittee + ",")
    file_pointer.write(commit_permittee_email + ",")
    file_pointer.write(allow_commit_date+"\n")

    if DataMiningModeSetting.total_commit_count < 3:
        print(commit_datetime)
        print(commit_date)


######## ============== ########
# GitHubAPIでコミット情報をCSVとJSONファイルに書き込む
# DataMiningModeSetting.repo_url_page_num：ページを変化させていく．
######## ============== ########
def GitHubAPI_Commit_Data_To_JSON_File():
    file_pointer = open(DataMiningModeSetting.file_path_csv, "w")
    file_pointer.write("commit_author,")
    file_pointer.write("commit_author_email,")
    file_pointer.write("commit_date,")
    # file_pointer.write("commit_message,")
    file_pointer.write("commit_message_words,")
    file_pointer.write("commit_permittee,")
    file_pointer.write("commit_permittee_email,")
    file_pointer.write("commit_permission_date\n")
    # WriteFileCSVHeader(file_pointer)
    DataMiningModeSetting.repo_url_page_num = 1
    while DataMiningModeSetting.API_Link_Count >= DataMiningModeSetting.repo_url_page_num:
        # 各リポジトリのcommitを取得
        git_commits_url = "{0}{1}{2}?per_page={3}&page={4}{5}{6}".format(
            DataMiningModeSetting.GIT_FIXED_URL, DataMiningModeSetting.GIT_REPOSITORY, DataMiningModeSetting.GIT_GET_INFO_PREFIX, DataMiningModeSetting.GIT_GET_ONE_REQUESTS, DataMiningModeSetting.repo_url_page_num, DataMiningModeSetting.git_client_id_query, DataMiningModeSetting.git_client_secrets_query)
        git_commits = requests.get(git_commits_url).text
        commits = json.loads(git_commits)

        # API 取得がlimitを超えてしまった場合の例外処理
        if git_commits == "[]":
            CommonSetting.Error_message = '正常に全てのコミットデータを取得しました'
            break
        elif type(commits) != list and "API rate limit exceeded" in commits["message"]:
            print("Sorry, Today's Github API is limited...")
            CommonSetting.Error_message = "Sorry, Today's Github API is limited..."
            break
        else:
            pass

        # commitの内容を取得
        for commit in commits:
            # commitの取得件数を求める
            DataMiningModeSetting.total_commit_count += 1
            # WriteFileCSVGitHubData(file_pointer, commit)
            commit_datetime = datetime.datetime.fromisoformat(
                commit["commit"]["committer"]["date"].replace('Z', '+00:00')).astimezone(DataMiningModeSetting.jp)
            commit_author = commit["commit"]["author"]["name"] if commit["commit"]["author"]["name"] else ''
            commit_author_email = commit["commit"]["author"]["email"] if commit["commit"]["author"]["email"] else ''
            commit_date = commit["commit"]["author"]["date"] if commit["commit"]["author"]["date"] else ''
            commit_permittee = commit["commit"]["committer"]["name"] if commit["commit"]["committer"]["name"] else ''
            commit_permittee_email = commit["commit"]["committer"][
                "email"] if commit["commit"]["committer"]["email"] else ''
            allow_commit_date = commit["commit"]["committer"]["date"] if commit["commit"]["committer"]["date"] else ''
            commit_message = commit["commit"]["message"] if commit["commit"]["message"] else ''
            commit_message_words_num = len(
                commit_message) if len(commit_message) else 0
            file_pointer.write(commit_author+",")
            file_pointer.write(commit_author_email+",")
            file_pointer.write(commit_date+",")
            # file_pointer.write(commit_message + ",")
            file_pointer.write(str(commit_message_words_num) + ',')
            file_pointer.write(commit_permittee + ",")
            file_pointer.write(commit_permittee_email + ",")
            file_pointer.write(allow_commit_date+"\n")
            if DataMiningModeSetting.total_commit_count < 3:
                print(commit_datetime)
                print(commit_date)

        DataMiningModeSetting.repo_url_page_num += 1  # paginationを進める

    file_pointer.close()
