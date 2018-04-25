# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function
import socket
from contextlib import closing
#import commands # python2.x
import shlex
import subprocess
import time
from time import sleep
import sys
import urllib
#import xml.etree.ElementTree as ET

import xmltodict
from xml.parsers.expat import ExpatError,errors
import json

BUFSIZE = 4096

julius = None
julius_socket = None

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


def delete_socket(c):
    c.close()


def invoke_julius():
    print ('INFO : invoke julius')
    #args = r'ALSADEV=\"plughw:1,0\" /usr/local/bin/julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module'
    #args = r'/usr/local/bin/julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module'
    args = 'julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module' # 環境変数設定版
    #args = 'julius -C ~/grammar-kit-4.3.1/testmic.jconf -nostrip -module' # 辞書なし版

    p = subprocess.Popen(
            #shlex.split(args),
            args,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
    time.sleep(2.0) # Juliusの起動待ち
    print ('INFO : invoke julius complete')
    return p


def invoke_julius_set():
    # プロセスの用意
    julius = invoke_julius()
    # ソケット通信の接続を行う
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # TCPサーバー接続の初期化
        s.connect(('localhost', 10500))
    except:
        print("ERRER :ソケット接続のエラーが発生したため終了します") # ERR 111
        import traceback
        traceback.print_exc()

        stdout_data, stderr_data = julius.communicate(timeout=2) # sec
        print ("communicate out : ",stdout_data)
        print ("communicate err : ",stderr_data)

        sys.exit(0)

    # ソケット接続に関連した文書を作成する。
    sf = s.makefile('rb')

    return (julius, s, sf)


def main():
    global julius
    global julius_socket
    # Juliusの起動スクリプトを実行する
    #activate_command = "ALSADEV=\"plughw:1,0\" julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module"
    #activate_command = ["ALSADEV=\"plughw:1,0\"","julius","-C","~/grammar-kit-4.3.1/testmic.jconf","-gram","~/dict/greeting","-nostrip","-module"]

    #print(activate_command)
    #command('sh start_julius.sh')
    #command(activate_command)
    #sleep(3)
#    invoke_julius()

    julius, julius_socket, sf = invoke_julius_set()


    # サーバからのデータ受信
    print("データ受信を開始します")
    data = ""
    while True:
        # ソケット通信でデータを受信するまで待機
        try:
            # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x83 in position 7: invalid start byte
            data = data + julius_socket.recv(BUFSIZE).decode('utf-8')
        except ConnectionResetError:
            print("ConnectionResetError")
            print("もう一回起動してください")
            sys.exit(0)
            # TODO もう一回起動するのが面倒なので、エラー吐いてもmainもう一回読み込むとかするコード書く

        #print("julius_socket START ************************************")
        #print(data)
        #print("julius_socket END   ************************************")

        #stdout_data, stderr_data = julius.communicate() # sec
        #print ("communicate out : ",stdout_data)
        #print ("communicate err : ",stderr_data)

        if julius.poll() is not None:   # means , julius dead
            delete_socket(julius_socket)
            julius, julius_socket, sf = invoke_julius_set()
        else:
            if "INPUT" in data:
                print("インプットってはいってたよ")

            #if "</RECOGOUT>\n." in data: TODO \n.省略したらifの中に入るようになったけど、これで本当に大丈夫か？
            if "</RECOGOUT>" in data:
                input_word = []
                print("録音が一段落したので、処理開始！！")
                try:
                    # xmlパーサにかけるために、必要な部分を抽出する
                    xml = data[data.find("<RECOGOUT>") : data.find("</RECOGOUT>") + len("</RECOGOUT>")]
                    print(xml)

                    dict_ = xmltodict.parse(xml) # raise ERR
                    print(json.dumps(dict_,indent=2))

                    for whypo in dict_['RECOGOUT']['SHYPO']['WHYPO']:
                        if whypo['@PHONE'] == 'silB':
                            continue
                        if whypo['@PHONE'] == 'silE':
                            continue
                        else:
                            input_word.append(whypo['@WORD']) # word type is <class 'str'>

                except ExpatError as err:
                    print("ErrorCode    :", errors.messages[err.code])
                    print("ErrorLineNum :", errors.messages[err.lineno])

                # 言葉を判別してどうこうするコードをここに書く
                for w in input_word:
                    print(w)

                data = ""
            else:
                pass # 録音が一段落するまではなにも処理しないことを明示


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("keyInterrupt Occured.")

        # サブプロセスを殺す
        # web情報では、killで終了しないjuliusのバグがある
        if julius != None:
            julius.kill()
        while julius.poll() is None:
            print ('INFO : wait for 0.1 sec julius\' termination')
            time.sleep(0.1)
        # ソケット通信のクライアントを閉じる
        delete_socket(julius_socket)

        print("INFO : Exit...")
        sys.exit(0)
