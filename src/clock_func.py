from datetime import datetime
import threading
import random
import time
import os

import audio
import jtalk
import filer
import day_list
import common_function as common

url_midnight    = audio.AUDIO_URL + "other/midnight"
url_evening     = audio.AUDIO_URL + "other/evening"
url_morning     = audio.AUDIO_URL + "other/morning"
url_daytime     = audio.AUDIO_URL + "other/daytime"

def specific_time(now):
    ''' 行事などがあったときのつぶやき '''

    '''
    if (now.month in json_list) == True:
        if (now.day in json_list) == True:
            print("行事***********************:")
    '''
# pythonならもっとここを綺麗に書けるのでは？
# 今日が何の日なのかと、設定されていたテキストを読み上げる
    for j in day_list.json_list:
        if j["month"] == now.month:
            if j["day"] == now.day:
                say_text = "今日は" + j["what"] + "です"
                jtalk.jtalk(say_text)
                say_text = j["voice"]
                jtalk.jtalk(say_text)
#*/


def time_signal(now):
    ''' 呼ばれると現在のhour,minuteを発音する '''
    # TODO wavファイルがないときは例外を投げるようにしたい
    audio.play( audio.AUDIO_URL + "Init/master.wav")
    say_text = str(now.hour%12) + '時' + str(now.minute) + "分です"
    jtalk.jtalk(say_text)


def mutter(now):
    ''' 呼ばれたら数分の1の確率で時間帯に合わせたことを何かつぶやく '''
    # 1 ~ 100 の整数値をランダムに生成
    rand_int = random.randint(1,100)
    if 1 <= now.hour and now.hour <=4 :
        # 真夜中の場合の一般リアクション
        # 0を割り算するとエラーが起こる可能性を考慮 
        if (rand_int % 3 == 0): 
            #print("真夜中")
            url = url_midnight
            url = filer.GetFileName(url)
            audio.play(url)
    elif 18 <= now.hour :
        # 夕方から夜にかけての場合の一般リアクション
        if (rand_int % 5 == 0):
            #print("夕方")
            url = url_evening
            url = filer.GetFileName(url)
            audio.play(url)
    elif 5 <= now.hour and now.hour <= 9 :
        # 朝の場合の一般リアクション
        if (rand_int % 5 == 0):
            #print("朝")
            url = url_morning
            url = filer.GetFileName(url)
            audio.play(url)
    else:
        # 昼の場合の一般リアクション
        if (rand_int % 6 == 0):
            #print("昼")
            url = url_daytime
            url = filer.GetFileName(url)
            audio.play(url)


def main():
    while 1:
        now = datetime.now()

        if now.minute%10 == 0:
            time_signal(now)
        elif random.randint(0,20) == 0:
            # 60分に一回程度で特殊日時ボイスを出します
            specific_time(now)
        else:
            mutter(now)

        time.sleep(60)


t_name = os.path.basename(__file__) + " : clock"
thread = threading.Thread(target=main, name=t_name)
thread.setDaemon(True)
thread.start()
if __name__=="__main__":
    time.sleep(1000) # for debug
