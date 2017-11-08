# -*- coding:utf-8 -*-  
 
import shlex
import subprocess
from datetime import datetime
CMD_SAY = 'sh ../bin/jtalk'

def say_datetime():
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    text = CMD_SAY + ' ' + text
    jtalk(text)
    return

def jtalk(text):
    command = CMD_SAY + ' ' + text
    print (command)
    proc = subprocess.Popen(shlex.split(command))
    proc.communicate()
    return

if __name__ == "__main__":
    say_datetime()

