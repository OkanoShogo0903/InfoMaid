import sys
#sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
# C:\Users\okano\Anaconda3\Lib\site-packages
from datetime import datetime
import locale
import time
import threading
import random
import os

#import jtalk
#import filer
import audio
import senser
import event_master as event
import common_function as common

import move_julius
import clock_func
import weather

#import news as news_file

#a = datetime.now()
#wea = weather.WeatherData()
# main function
def main():
    audio.playInitVoice()

    if 0:
        #print ("boice timer active")
        print (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        print (os.getcwd())
        print ("\n")

    # 天気しゃべらす
    wea.say(2)

    # ニュースしゃべらす
    new = news_file.NewsClass()
    new.say_news("ねとらぼ",1)


if __name__=="__main__":
    audio.playInitVoice()
    #main()
    #event.callWeather()
    time.sleep(10000)
    pass
