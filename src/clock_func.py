from datetime import datetime
import threading
import random
import time

import main
import audio
import jtalk
import filer
import day_list

now = datetime.now()
def clock():
    global now
    now = datetime.now()
#    global a
    print ("voice clock active")

    if(now.minute%10 == 0):
        time_signal()
    elif random.randint(0,20) == 0:
        # 60分に一回程度で特殊日時ボイスを出します
        specific_time()
    else:
        mutter()

    # 呼び出された後の処理
#    a = datetime.now()
    # 指定秒に呼び出されるようにスレッドをセットする
    t=threading.Timer(60,clock)
    t.start()

def specific_time():
# 行事などがあったときのつぶやき
    global now

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
def time_signal():
# 時報を行う
# TODO wavファイルがないときは例外を投げるようにしたい
    global now
    audio.play( main.AUDIO_URL + "Init/master.wav")
    say_text = str(now.hour%12) + '時' + str(now.minute) + "分です"
    jtalk.jtalk(say_text)
def mutter():
# つぶやき
    global now
    # 1 ~ 100 の整数値をランダムに生成
    rand_int = random.randint(1,100)
    if 1 <= now.hour and now.hour <=4 :
        # 真夜中の場合の一般リアクション
        # 0を割り算するとエラーが起こる可能性を考慮 
        if (rand_int % 3 == 0): 
            print("真夜中")
            url = main.AUDIO_URL + "other/midnight"
            url = filer.GetFileName(url)
            audio.play(url)
    elif 18 <= now.hour :
        # 夕方から夜にかけての場合の一般リアクション
        if (rand_int % 5 == 0):
            print("夕方")
            url = main.AUDIO_URL + "other/evening"
            url = filer.GetFileName(url)
            audio.play(url)
    elif 5 <= now.hour and now.hour <= 9 :
        # 朝の場合の一般リアクション
        if (rand_int % 5 == 0):
            print("朝")
            url = main.AUDIO_URL + "other/morning"
            url = filer.GetFileName(url)
            audio.play(url)
    else:
        # 昼の場合の一般リアクション
        if (rand_int % 6 == 0):
            print("昼")
            url = main.AUDIO_URL + "other/daytime"
            url = filer.GetFileName(url)
            audio.play(url)

if __name__=="__main__":
    specific_time(in1,in2)
