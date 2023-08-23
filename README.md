# table-definition-generator

## 概要
MySQLで構築しているRDBのテーブル定義をmarkdown形式で出力するツールです。  
テーブルごとに`SHOW FULL COLUMNS FROM {table_name};`で出力した代表的な項目と、  
`SHOW INDEX FROM {table_name};`で出力したインデックス定義を出力しています。  
論理名は各カラムのコメントを出力しています。  
読み込んでいるconfigファイル、および出力するテーブル定義ファイルの文字コードは`UTF-8`です。

## 動作確認環境

* 実装・実行環境：Windows 11
* Python：3.10.7
* MySQL：8.x

## 注意事項
リポジトリはpublicです。   
実際に使用されているテーブル情報などのプロジェクト情報は絶対にコミットしないでください。   
事故防止のため、.gitignoreファイルによって以下のファイルをGitの追跡対象から除外しています。

* outputディレクトリのsampleから始まるファイルを除く全てのファイル・ディレクトリ
* config.json
* packages（プロジェクト情報ではないがGit管理不要のため）

## 構成

```
.
├── output                             => 作成したファイルの出力先
│ └── sample_table-definition.md.md   => 出力ファイルサンプル
├── packages                           => 利用するパッケージの保存先
├── .gitignore                         => Git追跡除外設定ファイル
├── config_sample.json                 => config.json生成用のサンプルファイル
├── README.md                          => 本ページ
└── table-definition-generator.py      => メインスクリプト
```

## 使用方法

### 準備
1. `table-definition-generator` リポジトリをcloneする。
2. cloneしてきたディレクトリに移動する。（以下、同ディレクトリでの操作）
3. `pip install -r requirements.txt -t packages`を実行してパッケージを取得する。
   * グローバル領域に直接インストールしてよければ `pip install -r requirements.txt` 
4. `config.json` ファイルを作成し、必要な情報を入れる。
   * `config_sample.json` をコピーし、以下の情報を自身の使用環境に合わせて埋める。
      * "DB_HOST": テーブル情報を出力する対象DBのホスト名
      * "DB_USER": DBに接続する際のユーザー名
      * "DB_PASSWORD": DBに接続する際のパスワード
      * "DB_PORT": DBに接続する際のポート番号
      * "DB_NAME": 取得対象のテーブルがあるDB名
      * "OUTPUT_FILE":出力するファイル名

### 実行
1.  `python3 table-definition-generator.py`を実行する。
    *  Windows環境の場合、特に何も考えずにインストールしていたらpython3ではなくpythonコマンドだと思うので、`python table-definition-generator.py`を実行。（この辺りは環境に合わせて良きに調整してください）
2.  `output/` ディレクトリ内に`config.json`に定義した`OUTPUT_FILE`のファイル名でファイルが出力される。