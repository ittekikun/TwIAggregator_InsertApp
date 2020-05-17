TwIAggregator_InsertApp
====

TwIAggregatorのDB挿入アプリです。  
Python製です。

Copyright (c) 2020 ittekikun.

## Description
TwIAggregatorは表示アプリとDB挿入アプリが独立しており、こちらはDB挿入プログラムです。

## ※Warnning※
現在こちらのプログラムはベータ版となっております。
特にデータベース設計は現在考案中で、型の設定が甘かったり、APIから取得した生のjsonを入れておくカラムもそのままになっています。（仕様変更に対応するため）  
仮にデータベース設計を変更した場合は可能な限り移行をサポートする予定です。

## Requirement
* Python 3 (3.6で開発中)
* MariaDB (文字セットでutf8mb4を使えるように設定して下さい)

## Usage
### 初回実行時
1. イラストをRTする専用のアカウントを作成していくつかイラストをRTしておく
2. TwitterのAPIキーを取得する。(作成したアカウントとは別でも可)
3. データベースを設定する。（下記参照）
4. アプリを実行に必要なライブラリをインストール（下記参照）
5. insertDB.py上部にある設定項目を編集
6. 実行

### 定期実行
cron等で定期実行して下さい。

## Install
###データベース、テーブルを作成
※テーブル名は変更可能ですが、下記SQLとinsertDB.pyのSQLを自分で書き換える必要があります。
```SQL
CREATE TABLE `tweets` (
  `id` int(11) NOT NULL,
  `status_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `user_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tweet_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_urls` text COLLATE utf8_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `raw_json` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT;

ALTER TABLE `tweets`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `tweets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
```

###ライブラリをインストール
```bash
pip install -r requirements.txt
```

## License
[MIT](https://opensource.org/licenses/MIT)