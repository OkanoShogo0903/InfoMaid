# -*- coding: utf-8 -*-
import tweepy
from requests_oauthlib import OAuth1Session
import sys
sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
# C:\Users\okano\Anaconda3\Lib\site-packages
from datetime import datetime
import locale
import time
import threading
import random
class Tweet:
    def __init__(self):
        self.TEXT = ["世界へ挨拶",
        ]
        # ACCOUT : okanosyogo
        self.CK = 'oxzaxjtKBR067gYthawUZVWf1' # Consumer Key
        self.CS = 'duuaAVim00LhvM3YMwS2zJHdYHJ2rcCCazsVRrrQCxIoDrr49k' # Consumer Secret
        auth = tweepy.OAuthHandler(self.CK,self.CS)
        self.AT = ' 3107659669-tij5gWqxQoZLj12TkU6CZXKqPcxmfSB60ZcOaec' # Access Token
        self.AS = 'tKW58iLoAOvU661eukwWPi8BpcCHCMnb5KTGPO7BiIZCJ' # Accesss Token Secert
        auth.set_access_token(self.AT,self.AS)

        self.twitter = OAuth1Session(self.CK, self.CS, self.AT, self.AS)

        # ツイート投稿用のURL
        self.TWEET_URL = "https://api.twitter.com/1.1/statuses/update.json"
        # ツイート検索のURL
        self.SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
        #APIインスタンスを作成
        self.api = tweepy.API(auth)

    def twitter_func(self):
        # ツイート本文
        rand_int = random.randint(0,len(self.TEXT)-1)
        hoge = self.TEXT[rand_int]
        print(hoge)
        params = {"status": hoge}
    #    params = {"status": say text"}
        
        # OAuth認証で POST method で投稿
        req = self.twitter.post(self.TWEET_URL, params = params)

        # レスポンスを確認
        if req.status_code == 200:
            print (self.TEXT[rand_int])
        else:
            print ("Error: %d" % req.status_code)
        
    def timer(self):
        b = datetime.now()
    #    if(b.minute%5 == 0): # x分ごとに呼び出す
#        twitter_func()

        # 呼び出された後の処理
        # 指定秒に呼び出されるようにスレッドをセットする
        t=threading.Timer(60,timer)
        t.start()

    def test(self):
        # print(self.api.home_timeline()[0].text)
        try :
            self.api.update_status(status='世界に挨拶')
        except:
            import traceback
            traceback.print_exc()
        #タイムライン取得（最新10件）
        '''
        try :
            for tweet in tweepy.Cursor(self.api.user_timeline, id='okanosyogo').items(10):
                print (tweet.id) #id
                print (tweet.text) #本文
        except:
            import traceback
            traceback.print_exc()
        '''
    def search(self):
        search_word = "金沢"
        params = {'q': search_word,'count':'100',}

        req = self.twitter.get(self.SEARCH_URL, params = params)   # Tweetデータの取得
        if req.status_code == 200: # 成功した場合
            timeline = json.loads(req.text)
            metadata = timeline['search_metadata']
            statuses = timeline['statuses']
            limit = req.headers['x-rate-limit-remaining'] if 'x-rate-limit-remaining' in req.headers else 0
            reset = req.headers['x-rate-limit-reset'] if 'x-rate-limit-reset' in req.headers else 0              
            return {"result":True, "metadata":metadata, "statuses":statuses, "limit":limit, "reset_time":datetime.datetime.fromtimestamp(float(reset)), "reset_time_unix":reset}
        else: # 失敗した場合
            print ("Error: %d" % req.status_code)
            import traceback
            traceback.print_exc()
            return{"result":False, "status_code":req.status_code}

if __name__=="__main__":
    # twitter スレッドの動作始動
    tweet = Tweet()
    # tweet.timeline()
#    tweet.test()
#    tweet.twitter_func()
    tweet.search()
