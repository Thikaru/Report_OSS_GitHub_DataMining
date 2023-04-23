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
# データ分析モードの変数
import Setting.data_analysis_mode_settings as DataAnalysisModeSetting
# データ分析モードのページ
import Window.data_analysis_mode_window as DataAnalysisModeWindow


######## ==================== ########
# イベントハンドラ処理
######## ==================== ########
def DataAnalysisModeEventHandler():
    if CommonSetting.Event == '-analysis-json-mode-':
        print("-analysis-json-mode-")
        DataAnalysisModeWindow.MakeDataAnalysisCSVFileMDAPage()
    elif CommonSetting.Event == '-result-graph-viewer-':
        print("-result-graph-viewer-")
        DataAnalysisModeWindow.MakeDataAnalysisResultViewerMDAPage()
    elif CommonSetting.Event == '':
        print("TEST")
