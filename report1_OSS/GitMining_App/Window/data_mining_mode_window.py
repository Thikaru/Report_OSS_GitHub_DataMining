###############################
#### ライブラリ類           #####
###############################
import PySimpleGUI as sg

# 共通して使用する変数
import Setting.common_settings as CommonSetting
# DataMiningモード用変数を読み込む
import Setting.data_mining_mode_settings as DataMiningModeSetting


######## ============== ########
# 画像の前処理の設定をする画面
######## ============== ########
def MakeDataMiningSettingDMMPage():
    ## == ページのパーツ ==##
    col_topName = [
        [sg.Text('データマイニング設定(DMM)', font=(
            CommonSetting.HG_SEMI_CURSIVE, 40))],
    ]
    col_errorMessage = [
        [sg.Text(CommonSetting.Error_message,  font=(
            CommonSetting.HG_SEMI_CURSIVE, 20))]
    ]
    col_toTopPageButton = [
        [sg.Button('TOP PAGEへ', key='-top-page-', font=(CommonSetting.HG_SEMI_CURSIVE,
                   15), size=(20, 1))],
    ]
    col_settingParameter_a = [
        [sg.Text('CLIENT ID', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningModeSetting.CLIENT_ID, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-client-id-')],
        [sg.Text('CLIENT SECRET', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningModeSetting.CLIENT_SECRET, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-client-secret-')],
        [sg.Text('repository_user_name/repository_name/', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningModeSetting.GIT_REPOSITORY, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-repository-detail-')],
        [sg.Text('入手したい情報', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningModeSetting.GIT_GET_INFO_PREFIX, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-repository-info-prefix-')],
    ]
    col_settingParameter_b = [
        [sg.Text('初めの期間を指定', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningModeSetting.start_date, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-start_date-')],
        [sg.Text('終わりの期間を指定', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningModeSetting.finish_date, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-end-date-')],
        [sg.Text('1通信あたりのコミット情報獲得数', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningModeSetting.GIT_GET_ONE_REQUESTS, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-git-get-one-request-')],
        [sg.Text('API通信の制限を決める(5000が最大)', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningModeSetting.API_Link_Count, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-Api-link-count-')],
    ]
    col_inputFile = [
        [sg.Text("File", font=(CommonSetting.HG_SEMI_CURSIVE, 20)), sg.InputText(key='-input-data-preserve-csv-', enable_events=True, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(50, 1)),
         sg.FileBrowse('FileBrowse', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(20, 1), key='-input-preserve-csv-data-', target="-input-data-preserve-csv-", )]
    ]
    col_executeButton = [
        [sg.Button('上記の条件で処理を実行', font=(CommonSetting.HG_SEMI_CURSIVE, 20),
                   size=(20, 1), key='-execute-github-api-get-json-')]
    ]
    ## ================##

    ## ==ページ構成の枠組み==##
    edit_photo_page_layout = [[sg.Column(col_topName, justification='c')],
                              [sg.Column(col_toTopPageButton,
                                         justification='r')],
                              [sg.Column(col_errorMessage, justification='c')],
                              [sg.Column(col_settingParameter_a, justification='c'),
                               sg.Column(col_settingParameter_b, justification='c')],
                              [sg.Column(col_inputFile, justification='c')],
                              [sg.Column(col_executeButton, justification='c')]]
    CommonSetting.Page_index = 11
    CommonSetting.Window.close()
    CommonSetting.Window = sg.Window(
        'データマイニング設定ページ', edit_photo_page_layout, finalize=True, resizable=True, size=(CommonSetting.WINDOW_WIDTH, CommonSetting.WINDOW_HEIGHT))
    ## ==============##


def ResultGitHubDataMiningDMMPage():
    ## == ページのパーツ ==##
    col_topName = [
        [sg.Text('GitHubデータマイニングの結果ページ', font=(
            CommonSetting.HG_SEMI_CURSIVE, 40))],
    ]
    col_errorMessage = [
        [sg.Text(CommonSetting.Error_message,  font=(
            CommonSetting.HG_SEMI_CURSIVE, 20))]
    ]
    col_toTopPageButton = [
        [sg.Button('TOP PAGEへ', key='-top-page-', font=(CommonSetting.HG_SEMI_CURSIVE,
                   15), size=(20, 1))],
    ]

    col_settingParameter_a = [
        [sg.Text('CLIENT ID', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.CLIENT_ID, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('CLIENT SECRET', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.CLIENT_SECRET, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('repository_user_name/repository_name/', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.GIT_REPOSITORY, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('入手したい情報', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.GIT_GET_INFO_PREFIX, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('初めの期間を指定', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.start_date, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('終わりの期間を指定', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.finish_date, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('1通信あたりのコミット情報獲得数', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.GIT_GET_ONE_REQUESTS, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('API通信の制限を決める(5000が最大)', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.API_Link_Count, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('API通信回数結果', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.repo_url_page_num, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
        [sg.Text('コミット情報数', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
         sg.Text(DataMiningModeSetting.total_commit_count, font=(CommonSetting.HG_SEMI_CURSIVE, 20), )],
    ]
    # col_settingParameter_b = [
    #     [sg.Text('初めの期間を指定', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
    #      sg.Text(DataMiningModeSetting.start_date, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1))],
    #     [sg.Text('終わりの期間を指定', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
    #      sg.Text(DataMiningModeSetting.finish_date, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1))],
    #     [sg.Text('1通信あたりのコミット情報獲得数', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
    #      sg.Text(DataMiningModeSetting.GIT_GET_ONE_REQUESTS, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1))],
    #     [sg.Text('API通信の制限を決める(5000が最大)', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(30, 1)),
    #      sg.Text(DataMiningModeSetting.API_Link_Count, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1))],
    # ]

    col_button = [
        [sg.Button('もう一度GitHHubからデータを獲得するs', font=(CommonSetting.HG_SEMI_CURSIVE, 15), size=(
            25, 1), key='-data-mining-setting-mode-')],
    ]

    ## ================##

    ## ==ページ構成の枠組み==##
    edit_photo_page_layout = [[sg.Column(col_topName, justification='c')],
                              [sg.Column(col_toTopPageButton,
                                         justification='r')],
                              [sg.Column(col_errorMessage, justification='c')],
                              [sg.Column(col_settingParameter_a, justification='c'),
                               #    sg.Column(col_settingParameter_b, justification='c')
                               ],
                              [sg.Column(col_button, justification='c')],]
    CommonSetting.Page_index = 12
    CommonSetting.Window.close()
    CommonSetting.Window = sg.Window(
        'GitHubデータマイニングの結果ページ', edit_photo_page_layout, finalize=True, resizable=True, size=(CommonSetting.WINDOW_WIDTH, CommonSetting.WINDOW_HEIGHT))
    ## ==============##
