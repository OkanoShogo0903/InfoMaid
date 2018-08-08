# -*- coding: utf-8 -*-
from logging import (getLogger, StreamHandler, INFO, Formatter)

# ログの設定
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(Formatter("[%(asctime)s] [%(threadName)s] %(message)s"))
logger = getLogger()
logger.addHandler(handler)
logger.setLevel(INFO)


from threading import (Event, Thread)
import time


event = Event()
speech_recog_event = Event()
weather_event = Event()

def event_example1():
    logger.info("スレッド開始")
    event.wait()
    logger.info("スレッド終了")


def setSpeachRecog():
    # speech recog
    pass


def callSpeachRecog():
    speech_recog_event.set()


def callWeather():
    weather_event.set()


def publish(word):
    pass
#thread = Thread(target=event_example1)
#thread.start()
#time.sleep(3)
#logger.info("イベント発生")
#event.set()
