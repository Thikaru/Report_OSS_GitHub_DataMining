###############################
#### ライブラリ類           #####
###############################
import PySimpleGUI as sg

# 共通して使用する変数
import Setting.common_settings as CommonSetting
# OSS課題のデータマイニングで使用する変数読み込む
import Setting.data_mining_OSSReport_Setting as DataMiningOSSReportSetting


######## ============== ########
# GitHubリポジトリを選択する画面
######## ============== ########
def MakeDecideRepositoryDMORPage():
   ## == ページのパーツ ==##
    col_topName = [
        [sg.Text('データマイニングしたいOSSGitHubリポジトリ(DMOR)', font=(
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
    col_inputFile = [
        [sg.Text('GitHub作成者\n(例)[hashicorp]', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningOSSReportSetting.GitHub_Repository_creater, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-repository-creator-')],
        [sg.Text('GitHubリポジトリネーム\n(例)[terraform]', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(25, 1)),
         sg.InputText(default_text=DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-repository-name-')],
    ]
    col_executeButton = [
        [sg.Button('上記のGITHUBリポジトリで行う', font=(CommonSetting.HG_SEMI_CURSIVE, 20),
                   size=(20, 1), key='-data-mining-analysis-setting-')],
        [sg.Button('処理を終了する', font=(CommonSetting.HG_SEMI_CURSIVE, 20),
                   size=(20, 1), key='-data-mining-end-')]
    ]
    ## ================##

    ## ==ページ構成の枠組み==##
    edit_photo_page_layout = [[sg.Column(col_topName, justification='c')],
                              [sg.Column(col_toTopPageButton,
                                         justification='r')],
                              [sg.Column(col_errorMessage, justification='c')],
                              # [sg.Column(col_settingParameter_a, justification='c'),
                              #  sg.Column(col_settingParameter_b, justification='c')],
                              [sg.Column(col_inputFile, justification='c')],
                              [sg.Column(col_executeButton, justification='c')]]
    CommonSetting.Page_index = 31
    CommonSetting.Window.close()
    CommonSetting.Window = sg.Window(
        '設定ページ', edit_photo_page_layout, finalize=True, resizable=True, size=(CommonSetting.WINDOW_WIDTH, CommonSetting.WINDOW_HEIGHT))
    ## ==============##


######## ============== ########
# GitHubデータマイニングするデータを選択する画面
######## ============== ########
def MakeDecideDataMiningOptionDMORPage():
   ## == ページのパーツ ==##
    col_topName = [
        [sg.Text('データマイニングしたいデータを選択画面(DMOR)', font=(
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

    col_drop_down = [[sg.DropDown(
        DataMiningOSSReportSetting.data_mining_option, default_value=DataMiningOSSReportSetting.data_mining_option[DataMiningOSSReportSetting.data_mining_menu_option], key='-change-data-mining-option-', enable_events=True)]]

    col_inputFile_data_mining = []
    if DataMiningOSSReportSetting.data_mining_menu_option == 0:
        col_inputFile_data_mining = [
            [sg.Text('日毎のコミット数を累積棒グラフで出力する分析', font=(
                CommonSetting.HG_SEMI_CURSIVE, 20))],
            [sg.Text('日毎のコミット回数をCSVに保存する名前※.csvはあってもなくても良い', font=(CommonSetting.HG_SEMI_CURSIVE, 20)),
             sg.InputText(default_text='commit_num_per_date_'+DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-date-commit-csv-')],
            [sg.Text('日毎のコミット回数合計したものをCSVに保存する名前※.csvはあってもなくても良い', font=(CommonSetting.HG_SEMI_CURSIVE, 20)),
             sg.InputText(default_text='commit_num_per_date_sum_'+DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-date-commit-sum-csv-')],
            [sg.Text('作成された図を保存するファイル名を指定※.pngはあってもなくても良い', font=(CommonSetting.HG_SEMI_CURSIVE, 20)),
                sg.InputText(default_text="Commit_num_date_"+DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-date-commit-graph-')],
        ]
    elif DataMiningOSSReportSetting.data_mining_menu_option == 1:
        col_inputFile_data_mining = [
            [sg.Text('コミット数TOP10の棒グラフを分析', font=(
                CommonSetting.HG_SEMI_CURSIVE, 20))],
            [sg.Text('コミットを行った人のコミット数のデータを保存するCSVの名前※.csvはあってもなくても良い', font=(CommonSetting.HG_SEMI_CURSIVE, 20)),
             sg.InputText(default_text='creator_commit_num_'+DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-commiter-csv-')],
            [sg.Text('作成された図を保存するファイル名を指定※.pngはあってもなくても良い', font=(CommonSetting.HG_SEMI_CURSIVE, 20)),
                sg.InputText(default_text="Top10_Commit_" + DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-commit-top10-graph-')],
        ]
    elif DataMiningOSSReportSetting.data_mining_menu_option == 2:
        col_inputFile_data_mining = [
            [sg.Text('コミットメッセージの文字数の分布を分析', font=(
                CommonSetting.HG_SEMI_CURSIVE, 20))],
            [sg.Text('コミットメッセージと文字数のデータをCSVに保存する名前※.csvはあってもなくても良い', font=(CommonSetting.HG_SEMI_CURSIVE, 20)),
             sg.InputText(default_text="Commit_message_words" + DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-commit-message-csv-')],
            [sg.Text('コミット文字数の平均最大最小コミット数などを書き出すTXTに保存する名前※.txtはあってもなくても良い', font=(CommonSetting.HG_SEMI_CURSIVE, 20)),
             sg.InputText(default_text="Commit_message_MaxMin" + DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-commit-message-txt-')],
            [sg.Text('作成された図を保存するファイル名を指定※.pngはあってもなくても良い', font=(CommonSetting.HG_SEMI_CURSIVE, 20)),
                sg.InputText(default_text="Commit_message_words_" + DataMiningOSSReportSetting.GitHub_Repository_name, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(10, 1), key='-commit-message-graph-')],
        ]

    col_executeButton = [
        [sg.Button('上記のGITHUBリポジトリで行う', font=(CommonSetting.HG_SEMI_CURSIVE, 20),
                   size=(20, 1), key='-data-mining-analysis-')],
        [sg.Button('処理を終了する', font=(CommonSetting.HG_SEMI_CURSIVE, 20),
                   size=(20, 1), key='-data-mining-end-')]
    ]
    ## ================##

    ## ==ページ構成の枠組み==##
    edit_photo_page_layout = [[sg.Column(col_topName, justification='c')],
                              [sg.Column(col_toTopPageButton,
                                         justification='r')],
                              [sg.Column(col_errorMessage, justification='c')],
                              [sg.Column(col_drop_down, justification='c')],
                              [sg.Column(col_inputFile_data_mining,
                                         justification='c')],
                              [sg.Column(col_executeButton, justification='c')]]
    CommonSetting.Page_index = 32
    CommonSetting.Window.close()
    CommonSetting.Window = sg.Window(
        '設定ページ', edit_photo_page_layout, finalize=True, resizable=True, size=(CommonSetting.WINDOW_WIDTH, CommonSetting.WINDOW_HEIGHT))
    ## ==============##
