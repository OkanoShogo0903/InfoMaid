#from requests_oauthlib import OAuth1Session
#import sys
#sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
#from datetime import datetime
#import locale
#import time
#import threading
import json
import requests
from bs4 import BeautifulSoup
import jtalk

def SayWeather():
# 内容：天気と気温を読み上げる
# TODO 語尾や言い方にバリエーションを持たせるような造り込みがあるとおもしろい
    jtalk.jtalk("今日の天気をお伝えします")
    list_ = WeatherFunc()
    jtalk.jtalk("今日の天気は" + list_[0])
    if list_[1] != "不明":
        jtalk.jtalk("最高気温は" + list_[1] + "度")
    else:
        jtalk.jtalk("最高気温は" + list_[1] + "です")
        
    if list_[2] != "不明":
        jtalk.jtalk("最低気温は" + list_[2] + "度")
    else:
        jtalk.jtalk("最低気温は" + list_[2] + "です")
def WeatherFunc():
# 内容：天気に関するデータをweatherhackのAPIから手に入れる
    # jsonデータを取ってくる
    url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=170010"
    resp = requests.get(url)
    # print(resp.text)

    json_dict = json.loads(resp.text)

    telop = json_dict['forecasts'][0]['telop']

    try:
        tem_max = json_dict['forecasts'][0]['temperature']['max']['celsius']
        tem_max += '°'
    except TypeError:
        tem_max = "不明"

    try:
        tem_min = json_dict['forecasts'][0]['temperature']['min']['celsius']
        tem_min += '°'
    except TypeError:
        tem_min = "不明"

    output = [telop,tem_max,tem_min]
#    out_str = "天気 : " + telop + "\n" + "最高気温 : " + tem_max + "\n" + "最低気温 : " + tem_min
#    out_str = "天気は" + telop + "最高気温は" + tem_max + "最低気温は" + tem_min

    return output

if __name__=="__main__":
#    jtalk.jtalk(WeatherFunc())
    SayWeather()
