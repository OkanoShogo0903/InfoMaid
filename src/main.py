import sys
#sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
# C:\Users\okano\Anaconda3\Lib\site-packages
from datetime import datetime
import locale
import time
import threading
import random
import os

import audio
import clock_func
import jtalk
import filer
import weather
import news as news_file
AUDIO_URL = "../etcs/Audio/"

a = datetime.now()
wea = weather.WeatherData()
# main function
def main():
    if 0:
        print ("boice timer active")
        print (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        print (os.getcwd())
        print ("\n")

        url = AUDIO_URL + "Init/init_voice.wav"
        audio.play(url)

    # とりあえず時間しゃべらせとく
        b = datetime.now()
        say_text = str(b.hour%12) + '時' + str(b.minute) + "分です"
        jtalk.jtalk(say_text)

    # 天気しゃべらす
    wea.say(2)

    # ニュースしゃべらす
    new = news_file.NewsClass()
    new.say_news("ねとらぼ",1)

# threads start
    t=threading.Timer(1,clock_func.clock)
    t.start()

if __name__=="__main__":
    main()
