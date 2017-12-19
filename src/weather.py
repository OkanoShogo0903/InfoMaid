import time
import threading
import json
import requests
from bs4 import BeautifulSoup
import jtalk

class WeatherData:
    """ class of weather data and functions """
    def __init__(self):
        # シングルトンで書くと綺麗では？？
        # 天気データの取得
        self.get_weather_data()

    def get_weather_data(self):
    # 内容：天気に関するデータをweatherhackのAPIから手に入れる
        print("get_weather_data : start")
        # jsonデータを取ってくる
        url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=170010"
        resp = requests.get(url)
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
        print("@copyright")
        print(json_dict['copyright']['title'])
        print(json_dict['copyright']['provider'])

        # 一時間ごとにデータを更新するために１時間後に呼び出す
        t=threading.Timer(60*60,self.get_weather_data)
        t.start()
        print("get_weather_data : end")
        print()

    def say(self,say_range_):
    # 内容：天気と気温を読み上げる
    # TODO 語尾や言い方にバリエーションを持たせるような造り込みがあるとおもしろい
        
        jtalk.jtalk("本日の" + self.city + "の天気をお伝えします")

        # 天気情報はスラスラ読み上げた方が秘書っぽい感じがしていいので、連続して読み上げさせる
        try:
            say_text = ""
            for data in self.forecasts[:say_range_]:
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
            err_txt = "天気についてのエラーが発生しています"
            print(err_txt)
            jtalk.jtalk(err_txt)
            
#        jtalk.jtalk(self.description)
#------------------------------------------------------
# 外から呼び出される時のサンプル
if __name__=="__main__":
    weather = WeatherData()
    weather.say(1)
