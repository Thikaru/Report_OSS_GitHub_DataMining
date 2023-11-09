# 課題 3：工数予測

[TopPage に戻る](../README.md)

### 参考資料

- 課題内容のファイル：「/講義資料/課題 3：工数予測」
- 課題提出ファイルの場所:「/課題提出/第 3 回工数管理/定量的ソフトウェア開発法*50M23229*富田洸工数予測.pdf」

## 課題内容

- FakeMonden.csv もしくは DummydataMonden.csv を使用する
- 開発工数を予測する線形重回帰モデルを構築せよ
- 構築したモデルの予測精度を評価せよ
  - FakedataMonden.csv
    - モデル構築：2005 年-2011 年のデータを使う
    - モデル評価：2012 年ー 2013 年のデータを使う
  - DummydataMonden.csv
    - モデル構築：2014 年-2016 年のデータを使う
    - モデル評価：2017 年-2018 年のデータを使う
- 必要に応じて下記を実施せよ
  - データクリーニング
  - 変数の対数変換
  - 変数選択

## レポートに含めるべき内容

- なぜ・どのようにデータクリーニングしたか．
- なぜ・どのように変数選択したか
- 対数変換を行ったか
- どのようなモデル式が構築されたか
- モデルの解釈を考えてみる
- モデルの予測精度
  - 絶対誤差平均
  - 相対誤差平均
- 得られた知見感想など

## コード内容

### フォルダ構成

```Shell
AllCSV：使用するためのCSVデータはすべて文字コードをUTF8形式にしている．

CSV：CSVデータ

data_cleaning：

data_histgram：項目ごとのヒストグラムを作成するプログラム
	→ architect_hist.py：アーキテクト
	→ development_type_hist.py：開発種別
	→ main_language_hist.py：主開発言語
	→ industru_hist.py：業種
	→ request_hist.py：要求仕様
	→ year_hist.py：年代

images：項目ごとの分布などを確認するための画像

LastCSV：結果用のCSVデータを作成

amount_log.py：存在するデータのみを対数化する

amount.py：存在するデータを取り出す

data_cleaning_analysis.py：データ分析用のCSVを作成

data_cleaning_delete.py：データの中に「-1」があるものがある行データを削除

data_cleaning_pickup.py：データ分析用のCSVを作成

data_cleaning.py：全てのデータを2値化する
```
