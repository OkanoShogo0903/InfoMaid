# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import sys
sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
# C:\Users\okano\Anaconda3\Lib\site-packages
from datetime import datetime
import locale
import wave
import pyaudio
import time
import threading
import random

print ("bot active")
print (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
print ("\n")
text = ["text",
]

def twitter_func():
    CK = 'Ie5H016sEX1S7rPa2H1xDzhjP'                             # Consumer Key
    CS = 'pcWF2njdauUm2t3g5Pq4l2XxaPZOB1DRU6CVSsUlj64psVqVRJ'         # Consumer Secret
    # ユーザID
    AT = '908126063284199425-ObKYdsMWZVL0dTNlSVr5f6qm5ZonQcf' # Access Token
    # ユーザパスワード
    AS = 'v3UV7IwKbGUJ0Qdg1HTtO8YZOjaLwV11AsaFbigmpeqkn'         # Accesss Token Secert

    # ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"

    # ツイート本文
    rand_int = random.randint(0,len(text)-1)
    hoge = text[rand_int]
    print(hoge)
    params = {"status": hoge}
#    params = {"status": "Hello, World!"}

    # OAuth認証で POST method で投稿
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(url, params = params)

    # レスポンスを確認
    if req.status_code == 200:
        print (text[rand_int])
    else:
        print ("Error: %d" % req.status_code)

def bot_timer():
    b = datetime.now()
    if(b.minute%5 == 0): # x分ごとの時報
        twitter_func()
    # 呼び出された後の処理
    # 指定秒に呼び出されるようにスレッドをセットする
    t=threading.Timer(60,bot_timer)
    t.start()

# main function
t=threading.Timer(1,bot_timer)
t.start()
