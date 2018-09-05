# -*- coding: utf-8 -*-
import threading
import time

import event_master as event
import common_function as common

def main():
    ''' TODO: ここをnlpっぽい処理に書き換える '''
    # Voice input Waitting.
    weather = ["てんき"]
    news    = ["にゅーす"]
    clock   = ["じかん","たいむ"]
    twitter = ["ついったー"]

    while 1:
        # subscribe is blocking.
        word = event.subscribeSpeechRecog()
        common.log(word)
        if word in weather:
            event.callWeather()
        elif word in news:
            event.callNews()
        elif word in clock:
            event.callClock()
        elif word in twitter:
            event.callTwitter()


thread = threading.Thread(target=main, name="nlp")
thread.setDaemon(True)
thread.start()
