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


