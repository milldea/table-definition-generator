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

---

## sample(サンプルテーブル)

|論理名|物理名|型|キー制約|Null制約|その他制約|
|---|---|---|---|---|---|
|ID|id|int unsigned|PRI|NO|auto_increment|
|カラム1|column1|int|MUL|NO||
|文字列カラム2|column2|varchar(50)||YES||
|日時|column3|datetime|MUL|YES||
|カテゴリー|category|enum(<br>　'INFO',<br>　'WARN',<br>　'ALERT'<br>)||YES||
|作成日時|created_at|datetime||YES|DEFAULT_GENERATED|
|更新日時|updated_at|datetime||YES|DEFAULT_GENERATED on update CURRENT_TIMESTAMP|

|インデックス名|対象カラム名|複合キーのキー順序|
|---|---|---|
|PRIMARY|id|1|
|Sample_INDEX|column1|1|
|Sample_INDEX2|column3|1|
||column2|2|

### 【参考】サンプルテーブルの構成

```
CREATE TABLE IF NOT EXISTS `sample` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `column1` int NOT NULL COMMENT 'カラム1',
  `column2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '文字列カラム2',
  `column3` datetime DEFAULT NULL COMMENT '日時',
  `category` enum('INFO','WARN','ALERT') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'INFO' COMMENT 'カテゴリー',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `Sample_INDEX` (`column1`) USING BTREE,
  KEY `Sample_INDEX2` (`column3`,`column2`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='サンプルテーブル';

```