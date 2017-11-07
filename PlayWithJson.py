from requests_oauthlib import OAuth1Session
import sys
sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
from datetime import datetime
import locale
import time
import threading
import json
import requests
from bs4 import BeautifulSoup

def LoopFunc():
    WeatherFunc()
'''
    b = datetime.now()
    if(b.minute%5 == 0): # x分ごとの時報
        WeatherFunc()
    # 呼び出された後の処理
    # 指定秒に呼び出されるようにスレッドをセットする
    t=threading.Timer(60,LoopFunc)
    t.start()
'''
def WeatherFunc():
    # try:
    # 文字化け確認のため、ファイルに出力する
    f = open('text.txt', 'w') # 書き込みモードで開く
    # jsonデータを取ってくる
    url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=170010"
    resp = requests.get(url)
    # print(resp.text)

    json_dict = json.loads(resp.text)

    telop = json_dict['forecasts'][0]['telop']

    try:
        tem_min = json_dict['forecasts'][0]['temperature']['min']['celsius']
        tem_min += '°'
    except TypeError:
        tem_min = "不明"

    try:
        tem_max = json_dict['forecasts'][0]['temperature']['max']['celsius']
        tem_max += '°'
    except TypeError:
        tem_max = "不明"

    out_str = "天気 : " + telop + "\n" + "最高気温 : " + tem_max + "\n" + "最低気温 : " + tem_min
    f.writelines(out_str)

    TwitterFunc(out_str)
    '''
    title = json_dict['title']
    print (title)
    f.writelines(title)
    '''
    '''
    desc = json_dict['description']['text']
    print (desc)
    f.writelines(desc)
    '''

    # finally:
    #    json_dict.close()

    f.close()

def TwitterFunc(hoge):
    CK = 'tDjaAdzoiKz1yvgCgh1Lzp7YB'                             # Consumer Key
    CS = 'xOZ9Squ12MMLkGbZkLqbO60EOFfPdvTyVrodYtvroDg8YS61EV'         # Consumer Secret
    AT = '909665418821771269-zueREo9H8fcgt4MS2j1GAm81psQCCDN' # Access Token
    AS = 'v1zIgYzLCFM2CKjW91hMFqgXQIfvT8wixK3EPL7qsFFsw'         # Accesss Token Secert

    # ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"

    # ツイート本文
    print(hoge)
    params = {"status": hoge}
#    params = {"status": "Hello, World!"}

    # OAuth認証で POST method で投稿
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(url, params = params)

    # レスポンスを確認
    if req.status_code == 200:
        print ("OK")
    else:
        print ("Error: %d" % req.status_code)

# main function
t=threading.Timer(1,LoopFunc)
t.start()
