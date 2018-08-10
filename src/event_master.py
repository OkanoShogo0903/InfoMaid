# -*- coding: utf-8 -*-
from threading import (Event, Thread)
import time
import sys
import queue

import common_function as common

event = Event()
speech_recog_event  = Event()
weather_event       = Event()
wake_event          = Event()
go_out_event        = Event()
return_home_event   = Event()


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


# Speech Recognition Event--->>>
def callSpeachRecog():
    common.log(sys._getframe().f_code.co_name)
    speech_recog_event.set()


# Weather Event-------------->>>
def callWeather():
    common.log(sys._getframe().f_code.co_name)
    weather_event.set()


speech_queue = queue.Queue()
def publishSpeachRecog(_word):
    common.log(sys._getframe().f_code.co_name)
    speech_queue.put(_word)


def publish(word):
    pass
