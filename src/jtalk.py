# -*- coding:utf-8 -*-  
import re 
import shlex
import subprocess
from datetime import datetime
CMD_SAY = 'sh ../bin/jtalk'

def sayDatetime():
    # 現在の日付を出力する
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    jtalk(text)
    return


def command(_text):
    try:
        # OpenJTalkを利用するためのシェルコマンドを実行する
        command = CMD_SAY + ' ' + _text
        # subprocess.check_call()
        proc = subprocess.Popen(shlex.split(command))
        proc.communicate()
    except:
        print("audio command error")

    return


def jtalk(_origin):
# TODO 英語のスペルをそのまま読み上げるのをなんとかする（どじっ子）。辞書いれればなんとかなる？？
# TODO \『|\{正規化表現で『{でsplitできない？みたい

    # 長い文になると言葉が途切れ途切れになるため複数に分けて出力する
    text_list = re.split(r'\s|\[|\「', _origin)
#    text_list = re.split(r'\s|\.', _origin)
    # \s 空白
    # \[ 半角(
    
    for text in text_list:
#        text = text.replace(' ', '')
        text = text.replace(')', '')
        text = text.replace('（', '')
        text = text.replace('）', '')
        text = text.replace('」', '')
        text = text.replace('』', '')
        print(text)
        command(text)


if __name__ == "__main__":
    jtalk("ハローおはようございます my master")
    jtalk("ハロー「おは[よう」『ございます｛my master")
#    sayDatetime()

