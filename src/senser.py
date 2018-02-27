# -*- coding: utf-8 -*-
 
from datetime import datetime
import threading
import time
import RPi.GPIO as GPIO
from enum import Enum
 
# init
SENSOR_PORT=17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PORT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(SENSOR_PORT, GPIO.IN)

# 使用者は毎日家に帰ってくるとする
class Status(Enum):
    sleep = 1 # 寝てる
    home = 2 # 家で起きて活動している
    leave = 3 # 家にいない

def deinit():
    GPIO.cleanup()
 
def motion_sencer():
    res = GPIO.input(SENSOR_PORT)
    print ("MOTION SENCER : {}".format(res)) # 0,1
    return res

def sencer_thread():
    global status,motion_queue
    # 一日の終わりに状態のリセットをする
    now = datetime.now()
    if now.hour == 4 and now.minute == 0:
        status.value = status.sleep      

    # 小数点以下が欲しいので、1.0を掛けている
    # 人感センサの反応した割合 = (1の個数/全体の個数)*100
    # TODO motion_queue.count(x)では、60*60で3600回処理しているので、スレッドで回すなら処理数を下げるか？ → 速度図ってから → そんなにかかってない
    
    motion_rate_long = 1.0 * motion_queue.count(1) / len(motion_queue)
    motion_rate_short = 1.0 * (motion_queue[:short_valid_time]).count(1) / len(motion_queue[:short_valid_time])

    if status == Status.sleep:
        if motion_rate_short >= 0.4: # 朝起きたと判断する条件
            status = Status.home
            # ~~~ ここが起きたタイミング！！！ ~~~

    elif status == Status.home:
        if motion_rate_long <= 0.05: # 外出したと判断する条件
            status = Status.leave

    elif status == Status.leave:
        if motion_rate_short >= 0.2: # 帰ってきたと判断する条件
            status = Status.home
            # ~~~ ここが帰ってきたタイミング！！！ ~~~

    # センサーのデータ取得
    motion_queue.insert(0, motion_sencer()) # キューの先頭にデータをいれる
    motion_queue.pop(-1) # 一番古いデータを抜く

    if 0: # print out
        print("SENCER hit rate long  : {}".format(motion_rate_long))
        print("SENCER hit rate short : {}".format(motion_rate_short))
        print("SENCER status name    : {}".format(status))
    print("SENCER active count in one hour : {}".format(motion_queue.count(1)))

    t = threading.Timer(1,sencer_thread) # x秒毎でサンプリング
    t.start()

# MainFunc
# センサーデータの保存時間
long_valid_time = 60*60 # 60*60(sec) = 1(hour)
short_valid_time = 5 # x(sec)
status = Status(1) # プログラム起動時は家で起きているので、状態はhome=1の1にする
motion_queue = [1]*long_valid_time # defaultで個の1が入ったキュー

sencer_thread()
