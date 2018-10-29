# -*- coding:utf-8 -*-  
import re 
import shlex
import subprocess
from datetime import datetime
import threading
import sched
import time

CMD_SAY = 'sh ../bin/jtalk'
WORD_INTERVAL_SEC = 0.00

# Global Audio Function ----->>>
def sayDatetime():
    # 現在の日付を出力する
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    jtalk(text)
    return


def sayCommand(_text):
    try:
        # OpenJTalkを利用するためのシェルコマンドを実行する
        sayCommand = CMD_SAY + ' ' + _text
        # subprocess.check_call()
        proc = subprocess.Popen(shlex.split(sayCommand))
        proc.communicate()
    except:
        print("audio sayCommand error")

    return


def jtalk(_origin):
# TODO 英語のスペルをそのまま読み上げるのをなんとかする（どじっ子）。辞書いれればなんとかなる？？
# TODO \『|\{正規化表現で『{でsplitできない？みたい

    # 長い文になると言葉が途切れ途切れになるため複数に分けて出力する
    text_list = re.split(r'\s|\[|\「|。', _origin)
    #text_list = re.split(r'[\p{P}]', _origin)
#    text_list = re.split(r'\s|\.', _origin)
    # \s 空白
    # \[ 半角(
    print(text_list)
    
    for text in text_list:
        #text = text.replace('[\p{P}]', '') # 約物を対象
#        text = text.replace(' ', '')
        text = text.replace(')', '')
        text = text.replace('（', '')
        text = text.replace('）', '')
        text = text.replace('」', '')
        text = text.replace('』', '')
        print(text)
        if text == '':
            continue
        else:
            # 喋ることリストに登録する.
            print(text)
            schedule.enter(delay=0, priority=1, action=sayCommand, argument=(text,))


def audioSchedule():
    while 1:
        #print(schedule.queue)
        schedule.run() # blocking=True
        time.sleep(WORD_INTERVAL_SEC)


# Audio Thread ----->>>
schedule = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
# 外部から呼び出される時のためのスレッドの作成
thread = threading.Thread(target=audioSchedule, name="Audio")
thread.setDaemon(True)
thread.start()

if __name__ == "__main__":
    jtalk("ハロー「おは[よう」『ございます｛my master")
#    sayDatetime()
