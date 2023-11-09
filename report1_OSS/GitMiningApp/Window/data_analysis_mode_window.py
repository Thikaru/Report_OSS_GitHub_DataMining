###############################
#### ライブラリ類           #####
###############################
import PySimpleGUI as sg

# 共通して使用する変数
import Setting.common_settings as CommonSetting
# データ分析モードの変数を読み込む
import Setting.data_analysis_mode_settings as DataAnalysisModeSetting


######## ============== ########
# 画像の前処理の設定をする画面
######## ============== ########
def MakeDataAnalysisCSVFileMDAPage():
   ## == ページのパーツ ==##
    col_topName = [
        [sg.Text('データマイニングCSV読み込み(MDA)', font=(
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
        [sg.Text("File", font=(CommonSetting.HG_SEMI_CURSIVE, 20)), sg.InputText(key='-input-data-preserve-csv-', enable_events=True, font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(50, 1)),
         sg.FileBrowse('FileBrowse', font=(CommonSetting.HG_SEMI_CURSIVE, 20), size=(20, 1), key='-input-preserve-csv-data-', target="-input-data-preserve-csv-", )]
    ]
    col_executeButton = [
        [sg.Button('上記の条件で処理を実行', font=(CommonSetting.HG_SEMI_CURSIVE, 20),
                   size=(20, 1), key='-result-graph-viewer-')]
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
    CommonSetting.Page_index = 21
    CommonSetting.Window.close()
    CommonSetting.Window = sg.Window(
        '設定ページ', edit_photo_page_layout, finalize=True, resizable=True, size=(CommonSetting.WINDOW_WIDTH, CommonSetting.WINDOW_HEIGHT))
    ## ==============##


######## ============== ########
# 画像の前処理の設定をする画面
######## ============== ########
def MakeDataAnalysisResultViewerMDAPage():
   ## == ページのパーツ ==##
    col_topName = [
        [sg.Text('データマイニング結果表示(MDA)', font=(
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

    ## ================##

    ## ==ページ構成の枠組み==##
    edit_photo_page_layout = [[sg.Column(col_topName, justification='c')],
                              [sg.Column(col_toTopPageButton,
                                         justification='r')],
                              [sg.Column(col_errorMessage, justification='c')],

                              ]
    CommonSetting.Page_index = 22
    CommonSetting.Window.close()
    CommonSetting.Window = sg.Window(
        'リザルト画面', edit_photo_page_layout, finalize=True, resizable=True, size=(CommonSetting.WINDOW_WIDTH, CommonSetting.WINDOW_HEIGHT))
    ## ==============##
