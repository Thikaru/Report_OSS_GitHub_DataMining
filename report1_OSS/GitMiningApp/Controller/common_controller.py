###############################
#### ライブラリ類           #####
###############################
import PySimpleGUI as sg
# 共通して使用する変数
import Setting.common_settings as CommonSetting
# 共通ページの作成関数コード
import Window.common_window as CommonPage


######## ==================== ########
# イベントハンドラ処理
######## ==================== ########
def CommonEventHandler():
    if CommonSetting.Event == '-top-page-':
        print('-top-page-')
        # 初期化処理
        ResetErrorMessage()
        CommonSetting.Window.close()
        CommonPage.make_top_page_window()
    elif CommonSetting.Event == '':
        print("TEST")
    elif CommonSetting.Event == '':
        print("TEST")


######## ==================== ########
# エラーメッセージの文字列を，空白に変更
######## ==================== ########
def ResetErrorMessage():
    CommonSetting.Error_message = ''


######## ==================== ########
# 数かどうか判定する関数
######## ==================== ########
def IsNumber(value):
    if value == '':
        return False
    elif value.isdigit():
        return True
    else:
        return False


######## ==================== ########
# 数と空白かどうか判定する関数
######## ==================== ########
def IsNumberOrBlank(value):
    if value.isdigit() or value == '':
        return True
    else:
        return False
