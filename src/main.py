import sys
#sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
# C:\Users\okano\Anaconda3\Lib\site-packages
from datetime import datetime
import locale
import time
import threading
import random
import os

import move_julius
import common_function as common
import audio
#import clock_func
#import jtalk
#import filer
import weather
import event_master as event
#import news as news_file

#a = datetime.now()
#wea = weather.WeatherData()
# main function
def main():
    play_init_voice()

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
    #main()
    #event.callWeather()
    time.sleep(1000)
    pass
