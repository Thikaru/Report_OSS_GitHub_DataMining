# GUIライブラリ
import PySimpleGUI as sg
# 共通で使う変数を読み込む
import Setting.common_settings as CommonSettings


def make_top_page_window():
  ## == ページのパーツ ==##
    col_topName = [
        [sg.Text('GitHubデータマイニング課題ようアプリ', font=(
            CommonSettings.HG_SEMI_CURSIVE, 40))]
    ]
    col_topImage = [
        [sg.Image(filename='Image/oss_1200.png',)]
    ]
    col_button = [
        [sg.Button('GitHubリポジトリコミットデータをJSONで取得', font=(CommonSettings.HG_SEMI_CURSIVE, 15), size=(20, 1), key='-data-mining-setting-mode-'),
         sg.Button('GitHubのJSONデータ分析', font=(CommonSettings.HG_SEMI_CURSIVE, 15), size=(20, 1), key='-analysis-json-mode-')],
        [sg.Button('OSS課題用データマイニングモードへ', font=(CommonSettings.HG_SEMI_CURSIVE, 15), size=(
            20, 1), key='-github-data-mining-setting-'),
         sg.Button('終了', font=(CommonSettings.HG_SEMI_CURSIVE, 15), size=(20, 1), key='-Quit-')],
        # [sg.Button('終了', font=(CommonSettings.HG_SEMI_CURSIVE, 15),
        #            size=(20, 1), key='-Quit-')],
    ]
    ## ==================##

    ## ==ページ構成の枠組み==##
    top_page_layout = [[sg.Column(col_topName, justification='c')],
                       [sg.Column(col_topImage, justification='c')],
                       [sg.Column(col_button, justification='c')]
                       ]
    CommonSettings.Page_index = 0

    CommonSettings.Window = sg.Window('TOP PAGE', top_page_layout, finalize=True, resizable=True, size=(
        CommonSettings.WINDOW_WIDTH, CommonSettings.WINDOW_HEIGHT))
    ## ===================##
