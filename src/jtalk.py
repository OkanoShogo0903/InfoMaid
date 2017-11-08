# -*- coding:utf-8 -*-  
 
import shlex
import subprocess
from datetime import datetime
def main():
    say_datetime()
    return

def say_datetime():
    CMD_SAY = 'sh ../bin/jtalk'
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    text = CMD_SAY + ' ' + text
    print (text)
    proc = subprocess.Popen(shlex.split(text))
    proc.communicate()
    return

if __name__ == "__main__":
    main()

