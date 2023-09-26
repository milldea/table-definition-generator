import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "packages"))
# MySQLdbのインポート
import MySQLdb
import json
from enum import IntEnum

# region 環境情報を読み込み
config_json = open("config.json", "r", encoding="utf_8")
config = json.load(config_json)

# DBの環境情報
DB_HOST = config["DB_HOST"]
DB_USER = config["DB_USER"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_PORT = config["DB_PORT"]
DB_NAME = config["DB_NAME"]

# 出力するファイル名
OUTPUT_FILE = config["OUTPUT_FILE"]

# endregion


# region SQLで取得できる項目の列番号を定義
class C(IntEnum):
    """
    SHOW FULL COLUMNSで返ってくる項目
    """

    Field = 0
    Type = 1
    Collection = 2
    Null = 3
    Key = 4
    Default = 5
    Extra = 6
    Privileges = 7
    Comment = 8


class T(IntEnum):
    """
    SHOW TABLE STATUSで返ってくる項目（使うところだけ定義）
    """

    Name = 0
    Comment = 17


class I(IntEnum):
    """
    SHOW INDEXS ~~で返ってくる項目（使うところだけ定義）
    """

    Key_Name = 2
    Column_Name = 4


# endregion

# 処理開始
print("Start.")

# region データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT, database=DB_NAME
)
cursor = connection.cursor()
# endregion

# region テーブルの一覧を取得
table_name_list = []
table_comment_list = []

cursor.execute(
    """
    SHOW TABLE STATUS;
    """
)

for row in cursor:
    table_name_list.append(row[T.Name])
    table_comment_list.append(row[T.Comment])
# endregion

with open(f"output/{OUTPUT_FILE}", mode="w", encoding="utf_8") as file:
    # region テーブルごとにカラム定義を取得
    for table_name, table_comment in zip(table_name_list, table_comment_list):
        cursor.execute(
            f"""
            SHOW FULL COLUMNS FROM `{table_name}`;
            """
        )

        # テーブル名を出力
        file.write(f"## {table_name}({table_comment})\n")
        file.write("\n")

        # region カラム情報を出力
        file.write("|論理名|物理名|型|キー制約|Null制約|その他制約|\n")
        file.write("|---|---|---|---|---|---|\n")

        for row in cursor:
            # enumだった場合、そのまま出力すると見づらいので値ごとに改行を挟む
            type = row[C.Type]
            if "enum" in row[C.Type]:
                type = (
                    row[C.Type]
                    .replace("(", "(<br>　")
                    .replace(",", ",<br>　")
                    .replace(")", "<br>)")
                )

            file.write(
                f"|{row[C.Comment]} |{row[C.Field]}|{type}|{row[C.Key]} |{row[C.Null]}|{row[C.Extra]} |\n"
            )

        file.write("\n")
        # endregion

        # region Indexの情報を作成
        cursor.execute(
            f"""
            SHOW INDEX FROM `{table_name}`;
            """
        )
        file.write("|インデックス名|対象カラム名|複合キーのキー順序|\n")
        file.write("|---|---|---|\n")

        pre_key_name = ""
        key_name = ""
        key_order = 1

        for row in cursor:
            if pre_key_name == row[I.Key_Name]:
                # 前レコードと同じキーならキー順を一つ増やす
                key_order += 1
                # 同じキー名が続くと見づらいのでブランク
                key_name = " "
            else:
                # 前レコードと違うキーならリセット
                key_order = 1
                key_name = row[I.Key_Name]
            file.write(f"|{key_name}|{row[I.Column_Name]}|{key_order}|\n")
            pre_key_name = row[I.Key_Name]

        file.write("\n")
        file.write("\n")
        # endregion
    # endregion

# 接続を閉じる
connection.close()
print("Done.")
