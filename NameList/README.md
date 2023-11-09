# 名簿管理システム：大学の講義で作成したシステム

[TopPage に戻る](../README.md)

## 課題内容

- 名簿管理システム
- コマンドを使って操作を行うことができるシステムである．
- 名簿データとなる CSV は約 2800 人のデータが格納されている．
- 「名簿管理が自分だけ使えるプログラム」「サーバクライアントで一人づつなら使えるプログラム」「多重要求を受け入れるサーバクライアントプログラム」の 3 種類を作成している．
- アクセスするユーザのプログラムによって権限が異なるような仕組みも取り入れている．権限ごとにできることできないことが存在する．

### 機能一覧

コマンド一覧

- サーバクライアントシステムでない CLI のこれだけで動く名簿管理プログラム

  - %Q：<%Q> プログラムを終了
  - %C：<%C> 保存データ数を出力
  - %P：<%P number> 引数の数分データを出力(正の数：先頭から　負の数：後ろから 0 ならすべて)
  - %R：<%R filename>ファイルを読み込む
  - %W：<%W filename>現在保存データをファイルに書き出す
  - %S：<%S number> 引数の数の要素ごとにソートする
  - %O：<%O> 上書き許可，禁止を切り替える(default：禁止)

- サーバクライアントシステムで動く名簿管理プログラム
  - %Q：<%Q> プログラムを終了
  - %C：<%C> 保存データ数を出力
  - %P：<%P number> 引数の数分データを出力(正の数：先頭から　負の数：後ろから 0 ならすべて)
  - %R：<%R filename>ファイルを読み込む
  - %W：<%W filename>現在保存データをファイルに書き出す
  - %S：<%S number> 引数の数の要素ごとにソートする
  - %O：<%O> 上書き許可，禁止を切り替える(default：禁止)
  - %A：<%A> 権限変更，管理者のみ使用可能

### 実行手順

- 名簿管理プログラム：サーバクライアントシステムでない CLI のこれだけで動く名簿管理プログラム

```Shell
gcc NameList_Management.c -o NameList_Management.exe
./NameList_Management.exe
```

- SimpleServerClient：サーバ・クライアントシステムが一度に 1 つごとなら通信が行える

```Shell
// server側を先に起動して，通信の待ち状態にする
gcc server.c -o server.exe
./server.exe

// client側　通信待ちのサーバに通信をする．
gcc client.c -o client.exe
./client.exe
```

- NAMELIST_MULTI_2021_12_31：多重応答が行える名簿管理システム

```Shell
// server側を先に起動して，通信の待ち状態にする
gcc server.c -o server.exe
./server.exe

// client1側　通信待ちのサーバに通信をする．
gcc client.c -o client.exe
./client.exe

// client2側　通信待ちのサーバに通信をする．
gcc client.c -o client.exe
./client.exe

// client3側　通信待ちのサーバに通信をする．
gcc client.c -o client.exe
./client.exe
```

### ファイルごとの説明

```Shell
FIN(MultiResponse)
	→NAMELIST_MULTI_2021_12_31：多重応答が行える名簿管理システム
		→ client1：クライアントプログラム
		→ client2：クライアントプログラム
		→ client3：クライアントプログラム
		→ server：サーバプログラム

SimpleServerClient：サーバ・クライアントシステムが一度に1つごとなら通信が行える
	→NAMELIST_FIN_2021_12_31
		→ client：クライアントプログラム
		→ server：サーバプログラム

名簿管理プログラム：サーバクライアントシステムでないCLIのこれだけで動く名簿管理プログラム
	→ FIN_SimpleNameList_Management
```
