# -*- coding: utf-8 -*-
 
from datetime import datetime
import threading
import time
import RPi.GPIO as GPIO
 
# init
SENSOR_PORT=14
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PORT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(SENSOR_PORT, GPIO.IN)

# 他のプログラムから参照されるフラグ
is_leave = False
is_come = False
is_wakeup = True # プログラム起動時には既に起きてるからTrur

# おでかけ検知
def get_leave_home():
    return is_leave
# 帰宅検知
def get_come_home():
    return is_come
# 起床検知
def get_wakeup():
    return is_wakeup

def deinit():
    GPIO.cleanup()
 
def sencer_check():
    if GPIO.input(SENSOR_PORT) == GPIO.HIGH :
        print ("OK {}".format(GPIO.input(SENSOR_PORT)))
    else :
        print ("NG {}".format(GPIO.input(SENSOR_PORT)))

def sencer_thread():
    # 一日の終わりに各フラグのリセット
    now = datetime.now()
    if now.hour == 4 and now.minute == 0:
        is_leave = false
        is_come = false
        is_wakeup = false

    # センサーのデータ取得
    sencer_check()

    t = threading.Timer(200,sencer_thread) # x秒毎でサンプリング
    t.start()
    
if __name__ == '__main__':
#  sys.exit(led_indicator())
#    led_init()
    t = threading.Timer(1,sencer_thread)
    t.start()
