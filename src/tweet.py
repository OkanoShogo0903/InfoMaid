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
import geophysics
import json
#import random
#import twitter

    # できること
    #   ・自分へ返信があったら読み上げる
    #   ・たまに最新のタイムラインをいくつか読み上げる（初期のつぶやき機能の感じ）
    #   ・ツイッターのワード検索（オプションとして位置などを指定できる）
    # geophysics.pyで緯度経度をjson取得してリストで返すようにする
    # 自分に対する返信を読み上げる

    # TODO
    # 直近のタイムラインを読み上げる
    # タイムラインが更新されたら読み上げる関数（使わんわ、没）
    # 特定ユーザの最新ツイートを検知する監視機能(いらんくね?)
    # timelineとmentionでかぶるものがあったら省く? メンションかタイムラインで一方だけを有効にするなら問題ない
    # URLと他人へのメンションとか消す
    # あと広告も消す
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
        latest = self.api.mentions_timeline(count=1)[0]
        self.timeline_threshold_time = latest.created_at
        self.mention_threshold_time = latest.created_at
        # スレッドを回しておく
        t = threading.Timer(1,self.twitter_thread)
        t.start()
    
#    # 自分のアカウントデータを表示する関数（試作品の意味合い強いです）
#    def my_account_data(self):
#        user = self.api.me()
#        # 自分のid
#        print(user.id) # 3107659669
#        # 自分の名前
#        print(user.name) # キッチン
#        print(user.screen_name) # okanosyogo
#        print(user.status.text)

       
    # ツイッターボット機能
    def tweet_bot(self):
        self.api.update_status(status = self.TEXT)

    def word_search(self,_word = "",_count = 10,_lang='ja',_result_type='popular',_address=None,_range=5.0):
        """ ツイッターの検索機能 """
        # _word : search _word
        # _count : search status count
        # _result_type : recent,popular,mixed
        # _address : 東京墨田区など町の名前

        # 指定が無いときはreturnする
        if _word == "" and _address == None:return
        # 住所や場所のキーワードが入力されているときは、GoogleMapApiから緯度経度を付与する
        if _address != None:
            geo_json = geophysics.get_geocode(_address)
            if geo_json == None:return
            lat = geo_json['results'][0]['geometry']['location']['lat']
            lng = geo_json['results'][0]['geometry']['location']['lng']
            geocode = "{},{},{}km".format(lat,lng,_range)
        else:
            geocode = None
            
        # _result_typeを指定するときはgeocodeを指定できない
        # _result_typeを有効にするとなにもでない？？
        result = self.api.search(q=_word, count=_count, lang=_lang, geocode=geocode)

        print(result)
        # if resultの結果が0ではないとき:
        # 得られた結果の分だけ結果を出力する
        jtalk.jtalk("検索結果を読み上げます")
        for i,status in  enumerate(reversed(result)):
            print('TWEET---%3d---' % (i + 1))
            print('TWEET user name : {}'.format(status.user.name))
            print('TWEET text      : {}'.format(status.text))
            jtalk.jtalk("{}様より".format(status.user.name))
            jtalk.jtalk("{}".format(status.text))
        #else:
        #   jtalk.jtalk("検索結果を読み上げます")


    def timeline(self , _like_favo_threshold = -1 , _search_num = 5):
        """ 自分の新しいタイムラインを表示する機能 """
        # _like_favo_threshold  : ファボとリツイートを足して[_like_favo_threshold]以上のツイートだけを表示
        # _search_num : 最新[_search_num]件のデータを扱う
        result = self.api.home_timeline()
        for i,status in  enumerate(reversed(result[:_search_num])):
            # 投稿時間を見て、新しいメンションかどうかを判断する
            if status.created_at > self.timeline_threshold_time:
                self.timeline_threshold_time = status.created_at
                
                # ファボとリツイートの数をとる
                f = status.favorite_count
                r = status.retweet_count

                # 人気のツイートだけを表示
                if f + r >= _like_favo_threshold:
                    print('---%3d---' % (i + 1))
                    print('TWEET user name : {}'.format(status.user.name))
                    print('TWEET text      : {}'.format(status.text))
    #                print(status.favorite_count)
    #                print(status.retweet_count)

                    jtalk.jtalk("タイムラインが更新されました")
                    jtalk.jtalk("{}様より".format(status.user.name))
                    jtalk.jtalk("{}".format(status.text))


    def reaction_for_mentions(self):
        """ 自分に返信があったときに反応して読み上げるスレッド """
        result = self.api.mentions_timeline(count=5)
        for i,status in  enumerate(reversed(result)):
            # 投稿時間を見て、新しいメンションかどうかを判断する
            if status.created_at > self.mention_threshold_time:
                self.mention_threshold_time = status.created_at
                # プリントと読み上げを行う
                # TODO 逆順で複数のツイートを検知する -> reversed追加した
                print('---%3d---' % (i + 1))
                print('TWEET user name : {}',format(status.user.name))
                print('TWEET text      : {}',format(status.text))

                jtalk.jtalk("{}様より、メンションが確認されました".format(status.user.name))
                jtalk.jtalk("{}".format(status.text))

                #say_text = "メンションが確認されました。"
                #say_text += status.user.name + "から。"
                #say_text += self.format_text(status.text)
                #jtalk.jtalk(say_text) # 最新のmentionを読み上げる


    # twitterに関係する関数を回すスレッド
    def twitter_thread(self):
#        return
        self.reaction_for_mentions()
        self.timeline(_like_favo_threshold = 5, _search_num = 5)

        # スレッドを回しておく
        t = threading.Timer(60,self.twitter_thread)
        t.start()
    
    def format_text(self,text):
        # メンションの削除
        # ＠から始る、任意文字、任意の空白文字まで一個だけ消す
        # (例：@okanosyogo @handa1123 こんにちわ → @handa1123 こんにちわ)
        res = re.sub(r"(@[a-zA-Z0-9_]* )+","",text)
        res = re.sub(r"(@[a-zA-Z0-9_]*:)+","",text)
#        res = re.sub(r"(?:https?|ftp)://[A-Za-z0-9.-]*","",res)
        res = res.replace('RT', '')
        res = res.replace(' ', '')
        # TODO URLの削除
        return res
        
if __name__=="__main__":
    # twitter スレッドの動作始動
    tweet = Tweet()
#    tweet.tweet_bot()
#    tweet.test_house()
#    tweet.timeline(_like_favo_threshold = 5, _search_num = 20)
#    tweet.word_search(_word = "メイドインアビス OR ナナチ",_count = 10)
#    tweet.word_search(_word = "ナナチ",_address = "東京タワー",_count = 100,_range=10.0)
#    tweet.word_search(_word = "ナナチ",_count = 10)

    print(tweet.format_text("\
            RT @momoco_haru: 第２回 Modernistic Illustration Galleryで「手のひらの踊り子」というイラストが入選・そして優秀賞をいただきました。\
            3/01～3/07まで東京都美術館（上野）にて展示されるそうです。\
            https://t.co/H…\
            "))
