import os
import time
import threading
import json
import requests
from bs4 import BeautifulSoup
#import Event
#from threading import (Event, Thread)

import jtalk
import common_function as common
import event_master as event

class WeatherData:
    """
        外部からweather_eventイベントを呼び出されると、
        今日と明日の天気・気温を言う。
    """
    URL = "http://weather.livedoor.com/forecast/webservice/json/v1?city=170010"
    def __init__(self):
        # シングルトンで書くと綺麗では？？
        # 天気データの取得
        self.getWeatherData()

        # 外部から呼び出される時のためのスレッドの作成
        self.thread = threading.Thread(target=self.waitEventCall, name="WeatherEvent")
        self.thread.setDaemon(True)
        self.thread.start()


    def __enter__(self):
        # withステートメントで処理するための記述
        return self


    def __exit__(self, type, value, traceback):
        pass


    def waitEventCall(self):
        interval_sec = 60*60*3 # 3時間 ごとに更新
        while 1:
            while not event.weather_event.wait(interval_sec):
                self.getWeatherData()
            event.weather_event.clear()
            self.sayWeather(_say_range=1)


    def getWeatherData(self):
    # 内容：天気に関するデータをweatherhackのAPIから手に入れる
        # jsonデータを取ってくる
        resp = requests.get(self.URL)
        # print(resp.text)

        json_dict = json.loads(resp.text)

        # 元データを保存しておく(使わないかも)
        self.origin_dict = json_dict

        # 今日、明日、明後日のデータを使いやすく取っておく
        self.area = json_dict['location']['area']
        self.pref = json_dict['location']['prefecture']
        self.city = json_dict['location']['city']

        self.title = json_dict['title']
        self.link = json_dict['link']
        self.publicTime = json_dict['publicTime']

        self.description = json_dict['description']['text']
        self.descPublicTime = json_dict['description']['publicTime']

        self.forecasts = json_dict['forecasts']

        # コピーライトについて
        #print("@copyright")
        #print(json_dict['copyright']['title'])
        #print(json_dict['copyright']['provider'])

        #print("getWeatherData : end")


    def sayWeather(self, _say_range):
        ''' 
            機能：天気と気温を読み上げる

            TODO : 
            語尾や言い方にバリエーションを持たせるような造り込みがあるとおもしろい
        '''
        
        jtalk.jtalk("本日の" + self.city + "の天気をお伝えします")

        # 天気情報はスラスラ読み上げた方が秘書っぽい感じがしていいので、連続して読み上げさせる
        try:
            say_text = ""
            for data in self.forecasts[:_say_range]:
                # 「~最低気温不明、明日の~」の、『、』をつけるための処理
                # say_textになにかが入っていたら、をつける
                if say_text:
                    say_text += "、"
                say_text += data['dateLabel'] + "の天気は"
                try:
                    say_text += "最高気温" + data['temperature']['max']['celsius'] + "度、"
                except TypeError:
                    # 気温がnullだったときは例外処理
                    say_text += "最高気温不明、"

                try:
                    say_text += "最低気温" + data['temperature']['min']['celsius'] + "度"
                except TypeError:
                    # 気温がnullだったときは例外処理
                    say_text += "最低気温不明"
            else:
                say_text += "です"
                jtalk.jtalk(say_text)
        except:
            err_txt = "天気についての予期せぬエラーが発生しました"
            common.log(err_txt)
            jtalk.jtalk(err_txt)
            
#        jtalk.jtalk(self.description) # 詳細

#------------------------------------------------------
WeatherData()

if __name__=="__main__":
    ''' 外から呼び出される時のサンプル '''
    event.callWeather()

