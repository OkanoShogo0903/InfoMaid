# -*- coding: utf-8 -*-
 
from datetime import datetime
import threading
import time
import RPi.GPIO as GPIO
from enum import Enum
 
#GPIO.setup(SENSOR_PORT, GPIO.IN)

import event_master as event
import common_function as common
class Status(Enum):
    sleep = 1 # 寝てる
    home = 2 # 家で起きて活動している
    leave = 3 # 家にいない

status = Status(2) # プログラム起動時は家で起きているので、状態はhome=1の1にする

# 使用者は毎日家に帰ってくるとする
class MotionSencer():
    SENSOR_PORT = 17
    LONG_VALID_TIME = 60*60 # 60*60(sec) = 1(hour)
    SHORT_VALID_TIME = 5 # x(sec)
    SAMPLING_SEC = 1
    def __init__(self):
        # センサー初期化
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PORT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # センサーデータの保存時間
        self.queue = [1]*self.LONG_VALID_TIME # defaultでx個の1が入ったキュー

        # センサースレッド作成
        self.manageSencerThread()


    def __del__(self):
        # 作法に則ってcleanup
        GPIO.cleanup()

    
    def returnMotionSencerValue(self):
        ''' センサーポートを参照して、0か1を返す'''
        res = GPIO.input(self.SENSOR_PORT)
        #print ("MOTION SENCER : {}".format(res)) # 0,1
        return res


    def manageSencerThread(self):
        '''
            このスレッドを定期的に回して、センサーデータからいろいろしているよ
        '''
        # 日付またぎによるステータスのリセット
        self.judgeStatusReset()

        # センサーのデータ取得
        self.updateSencerData()

        # ステータスの更新
        self.updateStatus()

        # スレッドのセット
        #t_name = os.path.basename(__file__) + " : Sencer"
        t = threading.Timer(self.SAMPLING_SEC,self.manageSencerThread) # (第一引数)秒毎でサンプリング
        t.setDaemon(True)
        t.start()


    def judgeStatusReset(self):
        '''
            一日の終わりに状態のリセットをする.
            4時0分にリセットするようにしている.
        '''
        global status
        now = datetime.now()
        if now.hour == 4 and now.minute == 0:
            status.value = status.sleep      


    def updateSencerData(self):
        self.queue.insert(0, self.returnMotionSencerValue()) # キューの先頭にデータをいれる
        self.queue.pop(-1) # 一番古いデータを抜く


    def updateStatus(self):
        '''
            小数点以下が欲しいので、1.0を掛けている
            人感センサの反応した割合 = (1の個数/全体の個数)*100

            TODO self.queue.count(x)では、60*60で3600回処理しているので、
            スレッドで回すなら処理数を下げるか？ → 速度図ってから → そんなにかかってない

            現在条件をすごくてきとうに処理しているから、
            これを数学チックに処理したい

            あと、パラメータを関数内でいじくらなくちゃいけないのはきもい.
            ---> __init__かクラス共通変数でするべきか
        '''
        global status
        
        # 判断に使う値の計算
        motion_rate_long = 1.0 * self.queue.count(1) / len(self.queue)
        motion_rate_short = 1.0 * (self.queue[:self.SHORT_VALID_TIME]).count(1) / len(self.queue[:self.SHORT_VALID_TIME])

        # ステータス更新の判断部分
        if status == Status.sleep:
            if motion_rate_short >= 0.4: # 朝起きたと判断する条件
                status = Status.home
                event.callOwnerWake() # --------> Event call!!

        elif status == Status.home:
            if motion_rate_long <= 0.05: # 外出したと判断する条件
                status = Status.leave
                event.callOwnerGoOut() # --------> Event call!!

        elif status == Status.leave:
            if motion_rate_short >= 0.2: # 帰ってきたと判断する条件
                status = Status.home
                event.callOwnerReturnHome() # --------> Event call!!
        else: # ステータスが変わらないことを明記しておく
            pass

        # 標準出力
        if 0: # print out
            print("SENCER hit rate long  : {}".format(motion_rate_long))
            print("SENCER hit rate short : {}".format(motion_rate_short))
            print("SENCER status name    : {}".format(status))
            print("SENCER active count in one hour : {}".format(self.queue.count(1)))


# MainFunc
MotionSencer()
if __name__=="__main__":
    time.sleep(1000) # for debug
