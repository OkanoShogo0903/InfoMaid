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

AUDIO_URL = "../etcs/Audio/"

a = datetime.now()

# main function
def main():
    if 1:
        print ("boice timer active")
        print (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        print (os.getcwd())
        print ("\n")

        url = AUDIO_URL + "Init/init_voice.wav"
        audio.play(url)

    # とりあえずしゃべらせとく
        b = datetime.now()
        say_text = str(b.hour%12) + '時' + str(b.minute) + "分です"
        jtalk.jtalk(say_text)

# threads start
    t=threading.Timer(1,clock_func.clock)
    
    t.start()

if __name__=="__main__":
    main()
