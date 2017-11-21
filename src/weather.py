from requests_oauthlib import OAuth1Session
#import sys
#sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
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
 #   f = open('text.txt', 'w') # 書き込みモードで開く
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

    return out_str

if __name__=="__main__":
    jtalk.jtalk(WeatherFunc())

