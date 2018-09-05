# -*- coding: utf-8 -*-
from threading import (Event, Thread)
import time
import sys
import queue

import common_function as common

event = Event()
# sencer event --->
wake_event          = Event()
go_out_event        = Event()
return_home_event   = Event()

# other event --->
weather_event       = Event()
news_event          = Event()
clock_event          = Event()
twitter_event       = Event()

# Queue --->
speech_queue = queue.Queue()

# Sencer Event-------------->>>
def callOwnerWake():
    common.log(sys._getframe().f_code.co_name)
    wake_event.set()


def callOwnerGoOut():
    common.log(sys._getframe().f_code.co_name)
    go_out_event.set()


def callOwnerReturnHome():
    common.log(sys._getframe().f_code.co_name)
    return_home_event.set()


# Weather Event-------------->>>
def callWeather():
    common.log(sys._getframe().f_code.co_name)
    weather_event.set()


# News Event-------------->>>
def callNews():
    common.log(sys._getframe().f_code.co_name)
    news_event.set()


# Clock Event-------------->>>
def callClock():
    common.log(sys._getframe().f_code.co_name)
    clock_event.set()


# Twitter Event-------------->>>
def callTwitter():
    common.log(sys._getframe().f_code.co_name)
    twitter_event.set()


# Speech Queue -------------->>>
def publishSpeechRecog(_word):
    common.log(sys._getframe().f_code.co_name)
    try:
        speech_queue.put_nowait(_word)
    except queue.Full: # because of non blocking process.
        common.log("queue is Full!!!")
    common.log("published")


def subscribeSpeechRecog():
    common.log(sys._getframe().f_code.co_name)
    # Wait.
    word = speech_queue.get(block=True, timeout=None)
    return word
