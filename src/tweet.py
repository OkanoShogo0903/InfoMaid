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
        self.TEXT = ["(tweepyによるbotテスト中)"]
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

       
# 緯度と経度からツイートを検索する関数。緯度と経度をGoogleMapAPIから取得する際に渡す住所の文字列が日本語ではエラーになるため未実装
#    def geophysics_search():
#        result = self.api.search(q = "geocode:35.65858,139.745433,1.5km",count=100)
#        word = "geocode:35.65858,139.745433,0.5km" # TokyoTower
#        pos = "geocode:36.5310338,136.6284361,5.0km" # KIT libraryCenter
#        q = pos + " " + "ロボカップ"
#        result = self.api.search(q = q,count=100)
#        # count分だけ結果を出力する
#        for i,status in enumerate(result):
#            print('---%3d---' % (i + 1))
#            print(status.user.name)
#            print(status.text)
 
    # ツイッターボット機能
    def tweet_bot(self):
        self.api.update_status(status = self.TEXT)

    # 自分のタイムラインを表示する機能
    def print_timeline(self , like_favo_threshold = -1 , search_num = 5):
        # like_favo_threshold  : ファボとリツイートを足して[like_favo_threshold]以上のツイートだけを表示
        # search_num : 最新[search_num]件のデータを扱う
        time_line = self.api.home_timeline()
        for status in time_line[:search_num]:
            f = status.favorite_count
            r = status.retweet_count
            if f + r >= like_favo_threshold:
#                print(status.favorite_count)
#                print(status.retweet_count)
                print('TWEET user name : {}'.format(status.user.name))
                print('TWEET text      : {}'.format(status.text))

    # ツイッターの検索機能
    def print_word_search(self,word = '',count = 10,lang='ja',result_type='popular',address=''):
        # word : search word
        # count : search status count
        # result_type : recent,popular,mixed
        # address : 東京墨田区など町の名前
        # 指定が無いときはreturnする
        if word == '' and address == '':return
 #       if address != '':
 #           geo_json = geophysics.get_geocode(address)
 #           word = geo_json.~~~ + " " + word
        result = self.api.search(q = word, count = count, lang = lang, result_type = result_type)
        # count分だけ結果を出力する
        for i,status in  enumerate(reversed(result)):
            print('TWEET---%3d---' % (i + 1))
            print('TWEET user name : {}'.format(status.user.name))
            print('TWEET text      : {}'.format(status.text))

    # 自分に返信があったときに反応して読み上げるスレッド
    def reaction_for_mentions(self):
        result = self.api.mentions_timeline(count=5)
        for i,status in  enumerate(reversed(result)):
            # 投稿時間を見て、新しいメンションかどうかを判断する
            if status.created_at > self.threshold_time:
                self.threshold_time = status.created_at
                # プリントと読み上げを行う
                # TODO 逆順で複数のツイートを検知する -> reversed追加した
                print('---%3d---' % (i + 1))

                say_text = "メンションが確認されました。"
                say_text += status.user.name + "から。"
                say_text += self.format_text(status.text)
                jtalk.jtalk(say_text) # 最新のmentionを読み上げる

                print('TWEET user name : {}',format(status.user.name))
                print('TWEET text      : {}',format(status.text))

    # twitterに関係する関数を回すスレッド
    def twitter_thread(self):
        self.reaction_for_mentions()

        # スレッドを回しておく
        t = threading.Timer(60,self.twitter_thread)
        t.start()
    
    def format_text(self,text):
        # メンションの削除
        # ＠から始まって、任意の英数字以外、任意の空白文字まで一個だけ消す
        # (例：@okanosyogo @handa1123 こんにちわ → @handa1123 こんにちわ)
        res = re.sub(r'(^@\w* )+',"",text)
        # TODO URLの削除
        # TODO RTの削除
#       res = re.sub('RT', "", text)
        return res
        
if __name__=="__main__":
    # twitter スレッドの動作始動
    tweet = Tweet()
#    tweet.tweet_bot()
#    tweet.test_house()
#    tweet.print_timeline(like_favo_threshold = 5, search_num = 20)
#    tweet.print_word_search(word = "メイドインアビス OR ナナチ",count = 10)
#    tweet.print_word_search(address = "住吉",count = 10)

#    t = "@okanosyogo195 @handa1123 メンションのテスト @nanati"
#    print(t)
#    print(tweet.format_text(t))
#    jtalk.jtalk(say_text) # 最新のmentionを読み上げる

