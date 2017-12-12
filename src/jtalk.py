# -*- coding:utf-8 -*-  
 
import shlex
import subprocess
from datetime import datetime
CMD_SAY = 'sh ../bin/jtalk'

def say_datetime():
    # 現在の日付を出力する
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    text = CMD_SAY + ' ' + text
    jtalk(text)
    return

def command(text):
    # OpenJTalkを利用するためのシェルコマンドを実行する
    command = CMD_SAY + ' ' + text
    print (command)
    proc = subprocess.Popen(shlex.split(command))
    proc.communicate()
    return

def jtalk(origin):
# TODO 英語のスペルをそのまま読み上げるのをなんとかする（どじっ子）。辞書いれればなんとかなる？？
# TODO 『や「でsplitして、』」をreplaceする

    # 長い文になると言葉が途切れ途切れになるため複数に分けて出力する
    separate_chars = ['　',' '] # 『
    text_list = [] 
    # *******紙見ながらこのへんをなおして！！！！********
    for char in separate_chars:
        if char in origin:
            tmp = origin.split(char)
            text_list = tmp

    for text in text_list:
#        text = text.replace(' ', '')
        text = text.replace('(', '')
        text = text.replace(')', '')
        text = text.replace('（', '')
        text = text.replace('）', '')
        text = text.replace('」', '')
        text = text.replace('』', '')
        print(text)
        command(text)

if __name__ == "__main__":
    jtalk("ハロー　(おはよう) ございます　my （master）")
#    say_datetime()

