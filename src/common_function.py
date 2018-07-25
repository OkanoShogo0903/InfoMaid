# -*- coding: utf-8 -*-
import threading
import os
#print (thread.getName() + "die")

# ログの設定
from logging import (getLogger, StreamHandler, INFO, Formatter)
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(Formatter("[%(asctime)s] [%(threadName)s] %(message)s"))
logger = getLogger()
logger.addHandler(handler)
logger.setLevel(INFO)


def threadCreate(target, name):
    thread_name = name
    thread = threading.Thread(target = main, name=thread_name)
    thread.start()


def startFunction(request):
    create_speech_recog_thread()

    this_thread_name = threading.currentThread()
    while True:
        time.sleep(2)

        tlist = threading.enumerate()
        #if len(tlist) &lt; 2: break
        for t in tlist:
            if t is this_thread_name: continue
            print (t)


def log(string):
    logger.info(string)

