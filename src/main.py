import sys
#sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
# C:\Users\okano\Anaconda3\Lib\site-packages
from datetime import datetime
import locale
import time
import threading
import random
import os

# [Import base lib] ----->>>
import jtalk
#import filer
import audio
import senser
import event_master as event
import common_function as common

# [Import expand lib] ----->>>
# <<<--- システムウェイクアップフェイズに以降とか、起動フェイズ開始とか、そんな感じにバラエティーを持たせたい.
import clock_func
import weather
import nlp
import tweet
import news # 時間かかるやつ.
import move_julius

# [Main function] ----->>>
if __name__=="__main__":
    audio.playInitVoice()
    try:
        # 定期的にメインスレッド以外のスレッド情報を出力するだけ.
        main_thread_name = threading.currentThread()
        while 1:
            time.sleep(60) # [sec]
            tlist = threading.enumerate() # スレッド情報のリストを取得
            for t in tlist:
                if t is main_thread_name: continue
                print (t)
                pass
    except KeyboardInterrupt:
        # メインスレッドが<C-c>で落ちると、他のスレッドは全てデーモンスレッドなのでプログラムが終了する
        common.log("プログラム終了")
