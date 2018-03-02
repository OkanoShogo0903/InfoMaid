# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function
import socket
from contextlib import closing
#import commands # python2.x
import shlex
import subprocess
from time import sleep
import sys
import urllib
import xml.etree.ElementTree as ET
def command(_com):
    try:
        # コマンドを実行する
        # subprocess.check_call()
        #print("args : {}".format(shlex.split(_com)))
        #proc = subprocess.Popen(shlex.split(_com))
        proc = subprocess.Popen(command)
        proc.communicate()
    except:
        print("command error")

    return

def invoke_julius():
    print ('INFO : invoke julius')
#    args = julius_path + ' -C ' + jconf_path + ' -module '
    args = "ALSADEV=\"plughw:1,0\" julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module"
    p = subprocess.Popen(
            shlex.split(args),
            stdin=None,
            stdout=None,
            stderr=None
        )
    time.sleep(3.0)
    return p


def main():
    #activate_command = "ALSADEV=\"plughw:1,0\" julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module"
    #activate_command = ["ALSADEV=\"plughw:1,0\"","julius","-C","~/grammar-kit-4.3.1/testmic.jconf","-gram","~/dict/greeting","-nostrip","-module"]

    #print(activate_command)
    #command('sh start_julius.sh')
    #command(activate_command)
    #sleep(3)
#    invoke_julius()

    host = 'localhost'
    port = 10500
    bufsize = 409600
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # TCPサーバー接続の初期化
    sock.connect((host,port))

    # ソケット接続に関連した文書を作成する。
    sf = sock.makefile('rb')

    while True:
        # TCPデータを受信するまで待機し、受信データを文字列として返す
        recv_data = sock.recv(bufsize)
        print(recv_data)
        print("!!!!!!")

#        line = sf.readline().decode('utf-8')
#        print (line)
        # juliusの区切り文字で分割
#        sp = recv_data.split('.\n')
#        print(sp)

#        with urllib.request.urlopen(recv_data) as response:
#            XmlData = response.read()
#            root = ET.fromstring(XmlData)
#            print(root.tag,root.attrib)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("keyInterrupt")
        # TODO ソケット閉じる
        sys.exit(0)
