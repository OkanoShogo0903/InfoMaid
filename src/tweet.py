# -*- coding: utf-8 -*-
import tweepy
#from datetime import datetime
#from requests_oauthlib import OAuth1Session
#import sys
#sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
# C:\Users\okano\Anaconda3\Lib\site-packages
#from datetime import datetime
#import locale
#import time
import threading
import jtalk
import re # seiki
#import random
#import twitter

    # できること
    #   ・自分へ返信があったら読み上げる
    #   ・たまに最新のタイムラインをいくつか読み上げる（初期のつぶやき機能の感じ）
    #   ・ツイッターのワード検索（オプションとして位置などを指定できる）

    # TODO
    # タイムラインが更新されたら読み上げる関数（使わんわ、没）
    # 自分に対する返信を読み上げる
    # geophysics.pyで緯度経度をjson取得してリストで返すようにする
    # 特定ユーザの最新ツイートを検知する監視機能

class Tweet:
    # 初期設定で認証まわりを行う
    def __init__(self):
        self.TEXT = ["(聞こえますか...私は今、バイト先からあなたの脳内に直接語りかけています) (tweepyによるbotテスト中)"]
        # ACCOUT : okanosyogo
        CK = 'oxzaxjtKBR067gYthawUZVWf1' # Consumer Key
        CS = 'duuaAVim00LhvM3YMwS2zJHdYHJ2rcCCazsVRrrQCxIoDrr49k' # Consumer Secret
        AT = '3107659669-tij5gWqxQoZLj12TkU6CZXKqPcxmfSB60ZcOaec' # Access Token
        AS = 'tKW58iLoAOvU661eukwWPi8BpcCHCMnb5KTGPO7BiIZCJ' # Accesss Token Secert
        auth = tweepy.OAuthHandler(CK,CS)
        auth.set_access_token(AT,AS)

        self.api = tweepy.API(auth)

        # 閾時間の記憶
        latest_timeline = self.api.mentions_timeline(count=1)[0]
        self.threshold_time = latest_timeline.created_at
        # スレッドを回しておく
        t = threading.Timer(1,self.twitter_thread)
        t.start()
    
    # 自分のアカウントデータを表示する関数（試作品の意味合い強いです）
    def my_account_data(self):
        user = self.api.me()
        # 自分のid
        print(user.id) # 3107659669
        # 自分の名前
        print(user.name) # キッチン
        print(user.screen_name) # okanosyogo
        print(user.status.text)

    # 試作プログラムを雑に試すスペースです
    def test_house(self):
#        result = self.api.search(q = "geocode:35.65858,139.745433,1.5km",count=100)
#        word = "geocode:35.65858,139.745433,0.5km" # TokyoTower
        pos = "geocode:36.5310338,136.6284361,5.0km" # KIT libraryCenter
        q = pos + " " + "ロボカップ"
        result = self.api.search(q = q,count=100)
        # count分だけ結果を出力する
        for i,status in enumerate(result):
            print('---%3d---' % (i + 1))
            print(status.user.name)
            print(status.text)
        
    def tweet_bot(self):
        self.api.update_status(status = self.TEXT)

    # 自分のタイムラインを表示する機能
    def print_timeline(self , threshold = -1 , search_num = 5):
        # threshold  : ファボとリツイートを足して[threshold]以上のツイートだけを表示
        # search_num : 最新[search_num]件のデータを扱う
        time_line = self.api.home_timeline()
        for obj in time_line[:search_num]:
            f = obj.favorite_count
            r = obj.retweet_count
            if f + r >= threshold:
#                print(obj.favorite_count)
#                print(obj.retweet_count)
                print(obj.text)

    # ツイッターの検索機能
    def print_word_search(self,word = 'none',count = 10,lang='ja',result_type='popular'):
        # word : search word
        # count : search status count
        # result_type : recent,popular,mixed
        # word指定が無いときはreturnする
        if word == 'none':return
        result = self.api.search(q = word, count = count, lang = lang, result_type = result_type)
        # count分だけ結果を出力する
        for i,status in  enumerate(result):
            print('---%3d---' % (i + 1))
            print(status.user.name)
            print(status.text)

    # 自分に返信があったときに反応して読み上げるスレッド
    def reaction_for_mentions(self):
        result = self.api.mentions_timeline(count=5)
        for i,status in  enumerate(reversed(result)):
            # 投稿時間を見て、新しいメンションかどうかを判断する
            if status.created_at > self.threshold_time:
                self.threshold_time = status.created_at
                # プリントと読み上げ
                # TODO @から半角スペースまでの間を削除する
                # TODO 逆順で複数のツイートを検知する -> reversed追加した
                print('---%3d---' % (i + 1))

                # ＠から始まって、任意の英数字以外、任意の空白文字までを消したい(例：@okanosyogo こんにちわ)
                say_text = re.sub('^@\w$s','re',status.text)
#                say_text = say_text.replace('@* ','')
                jtalk.jtalk(say_text) # 最新のmentionを読み上げる

                print(status.user.name)
                print(say_text)
#            else:
#                print("none tweet")
                

    # twitterに関係する関数を回すスレッド
    def twitter_thread(self):
        self.reaction_for_mentions()

        # スレッドを回しておく
        t = threading.Timer(5,self.twitter_thread)
        t.start()
    
    def format_text(self,text):
        # メンションの削除
        res = re.sub(r'(^@\w* )+',"",text)
#       res = re.sub('RT', "", text)
        return res
        
if __name__=="__main__":
    # twitter スレッドの動作始動
    tweet = Tweet()
#    tweet.tweet_bot()
#    tweet.test_house()
#    tweet.print_timeline(threshold = 5, search_num = 20)
#    tweet.print_word_search(word = "メイドインアビス OR ナナチ",count = 10)

    t = "@okanosyogo195 @handa1123 メンションのテスト @nanati"
    print(t)
    print(tweet.format_text(t))
#    jtalk.jtalk(say_text) # 最新のmentionを読み上げる

