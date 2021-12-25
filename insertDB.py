# tweet_insert_app_C99 / insertDB.py
#
# 0.0.1
#
# Copyright (c) 2020 ittekikun.
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT

import os
import json
from datetime import datetime, timedelta
from os.path import splitext, basename
import tweepy
import MySQLdb

########################################################
# 最後に収集したツイートを保存しておくファイル名を設定します。
FILE_NAME = 'last.txt'

# リツイートを取得するアカウントを設定します。
# ※ユーザー名ではなくユーザーIDを指定する必要があります。
TARGET_USER = '1152529934474067969'

# データベースに登録する日付の時差を設定します。
# 例えば-1に設定した場合は2020/05/18にこのプログラムを実行した場合2020/05/17で登録されます。
TIME_DELTA = -1

# データベース設定
DB_CONFIG = {
    'host': 'localhost',
    'db': 'TwIAggregator',
    'user': 'user',
    'pass': 'pass',
}

# Twitter APIキー設定
# ※最後に半角スペース等が入っていないか確認して下さい。
API_KEYS = {
    'API_key': '000',
    'API_secret_key': '000',
    'Access_token': '000',
    'Access_token_secret': '000',
}
########################################################


def convert_url(raw_url):
    filename = basename(raw_url)

    ext = splitext(filename)[1][1:]
    without_ext_filename = splitext(filename)[0]

    new_url = 'https://pbs.twimg.com/media/' + without_ext_filename + '?format=' + ext

    return new_url


def insert_db(tweets_data):
    try:
        conn = MySQLdb.connect(host=DB_CONFIG['host'], db=DB_CONFIG['db'], user=DB_CONFIG['user'],
                               passwd=DB_CONFIG['pass'], charset='utf8mb4')
    except MySQLdb.Error as ex:
        print('MySQL Error: ', ex)

    cursor = conn.cursor()

    for row in (reversed(tweets_data)):
        cursor.execute('INSERT INTO tweets VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (None, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    conn.commit()
    cursor.close()
    conn.close()


target_path = os.path.join(os.path.dirname(__file__), FILE_NAME)

now_datetime = datetime.now() + timedelta(days=TIME_DELTA)
now_date = now_datetime.strftime('%Y-%m-%d')

auth = tweepy.OAuthHandler(API_KEYS['API_key'], API_KEYS['API_secret_key'])
auth.set_access_token(API_KEYS['Access_token'], API_KEYS['Access_token_secret'])
api = tweepy.API(auth)

f = open(target_path, 'r')
last_id = f.readline()
f.close()

num = 0
first_tweet_id = 0
media_urls = list()
tweets = list()

for i, status in enumerate(tweepy.Cursor(api.user_timeline, user_id=TARGET_USER, tweet_mode='extended').items(300)):
    if 'retweeted_status' not in status._json:
        continue

    tweet = status._json['retweeted_status']

    tweet_id = tweet['id_str']
    if i == 0:
        first_tweet_id = tweet_id
    if last_id != tweet_id:
        if 'extended_entities' in tweet:
            user = tweet['user']

            user_id = user['id_str']
            user_name = user['name']

            tweet_text = tweet['full_text']

            for media in tweet['extended_entities']['media']:
                if 'video_info' not in media:
                    image_url = convert_url(media['media_url_https'])
                    media_urls.append({'image': {'url': image_url}})
                else:
                    video_info = sorted(media['video_info']['variants'], key=lambda x: 'bitrate' in x and -x['bitrate'])
                    video_url = video_info[0]['url']
                    media_urls.append({'video': {'thumb': media['media_url_https'], 'url': video_url}})

            tweets.append([tweet_id, user_id, user_name, tweet_text, json.dumps(media_urls), now_date,
                           json.dumps(tweet, ensure_ascii=False)])
            media_urls.clear()

            num += 1
    else:
        break

if num == 0:
    print('収集数ゼロ')
    exit()

f = open(target_path, 'w')
f.write(first_tweet_id)
f.close()

print('収集数：' + str(num))

print('データベースに挿入します。')
insert_db(tweets)

# status_text = "本日のイラストのRT件数は" + str(num) + "件です。
# api.update_status(status=status_text)
# print(status_text)
