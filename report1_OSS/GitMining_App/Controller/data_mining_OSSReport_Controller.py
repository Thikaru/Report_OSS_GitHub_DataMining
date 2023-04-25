###############################
#### ライブラリ類           #####
###############################
import PySimpleGUI as sg
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
# 共通して使用する変数
import Setting.common_settings as CommonSetting
# 共通ページの作成関数コード
import Window.common_window as CommonPage
# データマイニングOSS課題で使用する変数を読み込む
import Setting.data_mining_OSSReport_Setting as DataMiningOSSReportSetting
import Window.data_mining_OSSReport_window as DataMiningOSSReportWindow


######## ==================== ########
# イベントハンドラ処理
######## ==================== ########
def DataMiningOSSReportEventHandler():
    if CommonSetting.Event == '-github-data-mining-setting-':  # TopPageから分析するリポジトリを入力するページへ
        print('-github-data-mining-setting-')
        DataMiningOSSReportWindow.MakeDecideRepositoryDMORPage()
    elif CommonSetting.Event == '-data-mining-analysis-setting-':  # リポジトリ選定後→リポジトリのクローンを行い成功したら→分析種類を選択
        print("-data-mining-analysis-setting-")
        # GitHubから指定したリポジトリをクローンする
        GithubRepositoryClone()
        DataMiningOSSReportWindow.MakeDecideDataMiningOptionDMORPage()
    elif CommonSetting.Event == '-change-data-mining-option-':
        print("-change-data-mining-option-")
        if CommonSetting.Value['-change-data-mining-option-'] == '日毎のコミット数を累積棒グラフで出力する分析':
            DataMiningOSSReportSetting.data_mining_menu_option = 0
        elif CommonSetting.Value['-change-data-mining-option-'] == 'コミット数TOP10の棒グラフを分析':
            DataMiningOSSReportSetting.data_mining_menu_option = 1
        elif CommonSetting.Value['-change-data-mining-option-'] == 'コミットメッセージの文字数の分布を分析':
            DataMiningOSSReportSetting.data_mining_menu_option = 2
        DataMiningOSSReportWindow.MakeDecideDataMiningOptionDMORPage()
    elif CommonSetting.Event == '-data-mining-analysis-':
        print("-data-mining-setting-")
        if DataMiningOSSReportSetting.data_mining_menu_option == 0:
            print("日毎のコミット数を累積棒グラフ出力")
            DatePerCommitOutputGraph()
            DataMiningOSSReportWindow.MakeDecideDataMiningOptionDMORPage()
        elif DataMiningOSSReportSetting.data_mining_menu_option == 1:
            print("コミット数TOP10の棒グラフを出力")
            CommitTop10OutputGraph()
            DataMiningOSSReportWindow.MakeDecideDataMiningOptionDMORPage()
        elif DataMiningOSSReportSetting.data_mining_menu_option == 2:
            print("コミットメッセージの文字数の分布を分析")
            CommitMessageRangeOutputGraph()
            DataMiningOSSReportWindow.MakeDecideDataMiningOptionDMORPage()
    elif CommonSetting.Event == '-data-mining-end-':
        print("-data-mining-end-")
        DeleteGithubRepository()
        CommonPage.make_top_page_window()
    elif CommonSetting.Event == 'ttt':
        print("Test")
    elif CommonSetting.Event == 'test':
        print("Test")


######## ==================== ########
# GitHubから指定したリポジトリをクローンする
######## ==================== ########
def GithubRepositoryClone():
    print("GitHubから指定したリポジトリをクローンする")
    # Git cloneする
    subprocess.run(['git', 'clone', DataMiningOSSReportSetting.GITHUB_CLONE_PREFIX +
                   DataMiningOSSReportSetting.GitHub_Repository_creater+'/'+DataMiningOSSReportSetting.GitHub_Repository_name], cwd='GitHubRepository')
    print('Git Clone終了 : ' + DataMiningOSSReportSetting.GITHUB_CLONE_PREFIX +
          DataMiningOSSReportSetting.GitHub_Repository_creater+'/'+DataMiningOSSReportSetting.GitHub_Repository_name)


######## ==================== ########
# GitHubから指定したリポジトリをクローンする
######## ==================== ########
def DeleteGithubRepository():
    print("GitHubからクローンしたものを削除する")
    # try:
    #     subprocess.run(
    #         ['rm', '-rf', DataMiningOSSReportSetting.GitHub_Repository_name], cwd='GitHubRepository', stdout=subprocess.PIPE)
    #     print("次のフォルダを削除しました． : " +
    #           DataMiningOSSReportSetting.GitHub_Repository_name)
    # except Exception as e:
    #     print("次の例外が発生しました:", e)


######## ==================== ########
# 日毎のコミット数を累積棒グラフ出力
######## ==================== ########
def DatePerCommitOutputGraph():
    print("日毎のコミット数を累積棒グラフ出力")
    result = subprocess.run(
        ["git", "log", "--pretty=format:\"%cd\"", "--date=short"], cwd='GitHubRepository/'+DataMiningOSSReportSetting.GitHub_Repository_name, stdout=subprocess.PIPE)
    # 出力を文字列に変換
    output = result.stdout.decode("utf-8")
    # 行ごとに分割し、日付でカウント
    counts = {}
    for line in output.strip().split("\n"):
        date = line.strip().replace('"', '')
        if date not in counts:
            counts[date] = 1
        else:
            counts[date] += 1

    file_terraform = open(
        'Output_Mining_Data/csv/commit_date/commit_num_per_date_terraform.csv', 'w')
    file_sum_terraform = open(
        'Output_Mining_Data/csv/commit_date/commit_num_per_date_sum_terraform.csv', 'w')
    file_terraform.write("date,commit_count\n")
    file_sum_terraform.write("date,commit_sum_count\n")

    sum_commit = 0
    commit_date_data = []
    # 結果を表示
    for date, count in reversed(counts.items()):
        sum_commit += count
        commit_date_data.append([int(count), date])
        file_terraform.write(date+","+str(count) + '\n')
        file_sum_terraform.write(date+","+str(sum_commit) + '\n')

    df = pd.DataFrame(commit_date_data, columns=['commits', 'date'])
    # 日時データをdatetime型に変換
    df['date'] = pd.to_datetime(df['date'])
    # 日ごとの累計コミット数を計算
    df['cum_commits'] = df['commits'].cumsum()

    # グラフを作成
    fig, ax = plt.subplots(figsize=(10, 7))  # figsizeで表の大きさを指定
    ax.plot(df['date'], df['cum_commits'])
    ax.grid(color='grey', linestyle='--', linewidth=0.5)  # グリッド線を灰色に設定

    # グラフ外の背景色を黒色に設定
    fig.patch.set_facecolor('lightblue')

    # 年ごとに縦線を引く
    years = pd.Series(df['date'].dt.year.unique())
    for year in years:
        ax.axvline(pd.Timestamp(f'{year}-01-01'),
                   color='grey', linestyle='--', linewidth=0.5)

    # x軸に年の部分だけを表示
    years = pd.Series(df['date'].dt.year.unique())
    ax.set_xticks([pd.Timestamp(f'{year}-01-01') for year in years])
    ax.set_xticklabels(years)
    # グラフのタイトルと軸ラベルを設定
    ax.set_title('Daily Cumulative Commits[Terraform]')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Commits')
    # X軸のラベルを90度回転して表示
    plt.xticks(rotation=30)
    # グラフの保存
    plt.savefig(
        "Output_Mining_Data/graph/commit_date/Commit_num_date_terraform.png")


######## ==================== ########
# コミット数Top10の棒グラフを出力
######## ==================== ########
def CommitTop10OutputGraph():
    # gitコマンドを実行し、結果をバイト文字列として取得
    output = subprocess.check_output(
        ['git', 'shortlog', '-s', '-n'], cwd='GitHubRepository/'+DataMiningOSSReportSetting.GitHub_Repository_name,)
    # バイト文字列を文字列に変換
    output = output.decode('utf-8')
    # 改行文字で分割してリストにする
    lines = output.split('\n')

    # コミット作成者のコミット数のCSVを作成
    file_terraform = open(
        'Output_Mining_Data/csv/commiter_info/creator_commit_num_'+DataMiningOSSReportSetting.GitHub_Repository_name+'.csv', 'w')
    file_terraform.write("author, commit_count\n")

    commiter_commit_rank = []
    x_data = []
    y_data = []
    for line in lines:
        tmp = line.split('\t')
        if len(tmp) >= 2:
            file_terraform.write(tmp[1]+','+str(int(tmp[0]))+'\n')
            x_data.append(tmp[1])
            y_data.append(int(tmp[0]))
    file_terraform.close()

    # 最初の10行を取得
    x_data = x_data[:10]
    y_data = y_data[:10]

    fig = plt.figure(figsize=(6, 12), facecolor='lightblue')
    plt.bar(x_data, y_data)

    # グラフのタイトルや軸ラベルを設定
    plt.title('Top 10 Commiters by Commit Count[Terraform]')
    plt.xlabel('Author')
    plt.ylabel('Commit Count')

    # X軸のラベルを90度回転して表示
    plt.xticks(rotation=30)

    plt.savefig(
        "Output_Mining_Data/graph/commiter_info/Top10_Commit_" + DataMiningOSSReportSetting.GitHub_Repository_name + ".png")


######## ==================== ########
# コミットメッセージの文字数の分布を分析
######## ==================== ########
def CommitMessageRangeOutputGraph():
    print('コミットメッセージの文字数の分布を分析')
    # Git logコマンドでコミットログを取得する
    vagrant_result = subprocess.run(['git', 'log', '--oneline'],
                                    cwd='GitHubRepository/'+DataMiningOSSReportSetting.GitHub_Repository_name, stdout=subprocess.PIPE)

    # コミットメッセージとコミットをCSVファイルに保存する
    commit_file_pointer = open(
        "Output_Mining_Data/csv/commit_message/Commit_message_num" + DataMiningOSSReportSetting.GitHub_Repository_name + ".csv", "w")
    commit_detail_file_pointer = open(
        "Output_Mining_Data/text/commit_message/Commit_message_MaxMin" + DataMiningOSSReportSetting.GitHub_Repository_name + ".txt", "w")

    commit_file_pointer.write("words,commit_message\n")
    # 各コミットメッセージの文字の長さを計算する
    commit_messages = vagrant_result.stdout.decode().split('\n')
    message_lengths = [len(message.split(' ', 1)[1])
                       for message in commit_messages if message]
    commit_count = 0  # コミットの個数をカウントする変数
    commit_words_sum = 0
    max = -10  # コミットメッセージの最大文字を求める
    min = 100000  # コミットメッセージの最小文字数を求める
    for line in message_lengths:
        commit_file_pointer.write(
            str(line)+','+commit_messages[commit_count] + '\n')
        commit_words_sum += line
        commit_count += 1
        if line > max:
            max = line

        if line < min:
            min = line
        # print(line)

    commit_file_pointer.close()

    hist, bin_edges = np.histogram(
        message_lengths, bins=range(0, max+10, 10))

    print("vagrant max : " + str(max))
    print("vagrant min : " + str(min))
    # 結果の表示
    for i, count in enumerate(hist):
        commit_detail_file_pointer.write(
            f"{bin_edges[i]} ~ {bin_edges[i+1]}: {count}" + '\n')
    commit_detail_file_pointer.write("コミットメッセージ文字数最大：" + str(max) + '\n')
    commit_detail_file_pointer.write("コミットメッセージ文字最小数：" + str(min) + '\n')
    commit_detail_file_pointer.write("コミット数合計：" + str(commit_count) + '\n')
    commit_detail_file_pointer.write(
        "コミット文字数平均：" + str(round(commit_words_sum/commit_count, 3)))

    commit_detail_file_pointer.close()

    # グラフのサイズを指定
    fig = plt.figure(figsize=(18, 6), facecolor='lightblue')
    # ヒストグラムの描画
    plt.bar(bin_edges[:-1], hist, width=10, align='edge')
    plt.xticks(np.arange(0, 420, 10))
    for i in range(len(hist)):
        plt.text(bin_edges[i], hist[i], str(hist[i]),
                 fontsize=10, ha='center', va='bottom')
    # 軸ラベルの設定
    plt.title('Commit Num Hist[Vagrant]')
    plt.xlabel('Words')
    plt.ylabel('Commit Num')
    # グリッド線の表示
    plt.grid(True)
    # グラフの保存
    plt.savefig(
        "Output_Mining_Data/graph/commit_message/Commit_message_num_" + DataMiningOSSReportSetting.GitHub_Repository_name + ".png")
