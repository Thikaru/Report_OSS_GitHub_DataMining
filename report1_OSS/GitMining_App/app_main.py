###############################
#### ライブラリ類           #####
###############################
import PySimpleGUI as sg

# 共通で使う変数を読み込む
import Setting.common_settings as CommonSettings
# モードごとの処理
import Controller.common_controller as CommonController
import Controller.data_analysis_mode_controller as DataAnalysisModeController
import Controller.data_mining_mode_controller as DataMiningController


## =================##
## GUI構成           ##
## =================##

###############################
#### 定数                  #####
###############################
# レイアウトのテンプレート
sg.theme('BrownBlue')

###############################
#### グローバル変数         #####
###############################

App_end_list = [None, '-Quit-', sg.WIN_CLOSED]


###############################
#### main処理              #####
###############################
if __name__ == '__main__':
    CommonController.CommonPage.make_top_page_window()

    while True:
        CommonSettings.Event, CommonSettings.Value = CommonSettings.Window.read()
        if CommonSettings.Event in App_end_list:
            break
        else:
            # 共通処理でのイベントなのかを判定
            CommonController.CommonEventHandler()
            # GitHubデータマイニング処理のイベントなのかを判定する
            DataMiningController.DataMiningModeEventHandler()
            # データ分析処理のイベントなのかを判定する
            DataAnalysisModeController.DataAnalysisModeEventHandler()
    CommonSettings.Window.close()
