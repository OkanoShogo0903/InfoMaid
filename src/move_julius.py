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
import os
import threading
import types
#import xml.etree.ElementTree as ET
import xmltodict
from xml.parsers.expat import ExpatError,errors
import json
import pprint

#import event_master
import event_master as event
import common_function as common

class JuliusController(object):
    def __init__(self):
        self.BUFSIZE = 4096
        self.julius = None
        self.julius_socket = None
        self.julius, self.julius_socket, self.sf = self.invokeJuliusSet()

        #self.thread = threading.Thread(target = self.word_manager, name="[Word " + str(WordClass.thread_num) + "]")
        #self.thread.start()


    def __enter__(self):
        # withステートメントで処理するための記述
        return self


    def __exit__(self, type, value, traceback):
        # サブプロセスを殺す
        # web情報では、killで終了しないjuliusのバグがある
        if self.julius != None:
            #self.julius.kill()
            pass
        while self.julius.poll() is None:
            #print ('INFO : wait for 0.1 sec julius\' termination')
            time.sleep(0.1)
        # ソケット通信のクライアントを閉じる
        self.deleteSocket(self.julius_socket)

        #print("INFO : Exit...")
        #sys.exit(0)

        #スレッドが停止するのを待つ
        #self.stop_event.set()
        #self.thread.join()

    
    def reboot(self):
        self.julius, self.julius_socket, self.sf = self.invokeJuliusSet()


    def deleteSocket(self,c):
        c.close()


    def invokeJulius(self):
        common.log('INFO : invoke julius')
        #args = r'ALSADEV=\"plughw:1,0\" /usr/local/bin/julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module'
        #args = r'/usr/local/bin/julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module'
        #args = 'julius -C ~/grammar-kit-4.3.1/testmic.jconf -nostrip -module' # 辞書なし版
        #args = 'ALSADEV=\"plughw:0,0\" julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module' # 環境変数設定版
        #args = 'ALSADEV=\"plughw:0,0\" julius -C ~/grammar-kit-4.3.1/testmic.jconf -nostrip -module -charconv SJIS UTF-8 '
        args = 'ALSADEV=\"plughw:0,0\" julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict_sjis/greeting -nostrip -module -charconv SJIS UTF-8 ' # charconv試し

        p = subprocess.Popen(
                #shlex.split(args),
                args,
                stdin=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
        time.sleep(2.0) # Juliusの起動待ち
        #common.log('INFO : invoke julius complete')
        return p


    def invokeJuliusSet(self):
        # プロセスの用意
        julius = self.invokeJulius()
        # ソケット通信の接続を行う
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # TCPサーバー接続の初期化
            s.connect(('localhost', 10500))
        except:
            common.log("ERRER :ソケット接続のエラーが発生したため終了します") # ERR 111
            import traceback
            traceback.print_exc()

            stdout_data, stderr_data = julius.communicate(timeout=2) # sec
            common.log("communicate out : ",stdout_data)
            common.log("communicate err : ",stderr_data)

            sys.exit(0)

        # ソケット接続に関連した文書を作成する。
        sf = s.makefile('rb')

        return (julius, s, sf)


    def operate(self):
        # サーバからのデータ受信
        data = ""
        while True:
            #time.sleep(0.1)
            # ソケット通信でデータを受信するまで待機
            try:
                # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x83 in position 7: invalid start byte
                # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x82 in position 126: invalid start byte
                data = data + self.julius_socket.recv(self.BUFSIZE).decode('utf-8')
                #data = data + julius_socket.recv(BUFSIZE).encode('utf-8')
                #print ('[utf-8 decode]')
            
            #except UnicodeDecodeError:
            #    data = data + julius_socket.recv(BUFSIZE).decode('cp932')
            #    print ('[cp932 decode]')

            except ConnectionResetError:
                common.log("ConnectionResetError")
                common.log("もう一回起動してください")
                #sys.exit(0)
                return -1

            #print("julius_socket START ************************************")
            #pprint.pprint(data)
            #print("julius_socket END   ************************************")

            #stdout_data, stderr_data = julius.communicate() # sec
            #print ("communicate out : ",stdout_data)
            #print ("communicate err : ",stderr_data)

            if self.julius.poll() is not None:   # means , julius dead
                self.deleteSocket(self.julius_socket)
                self.julius, self.julius_socket, self.sf = self.invokeJuliusSet()
            else:
                if "INPUT" in data:
                    #print("インプットってはいってたよ")
                    pass

                #if "</RECOGOUT>\n." in data: TODO \n.省略したらifの中に入るようになったけど、これで本当に大丈夫か？
                if "</RECOGOUT>" in data:
                    input_word = []
                    #print("録音が一段落したので、処理開始！！")
                    try:
                        # xmlパーサにかけるために、必要な部分を抽出する
                        xml = data[data.rfind("<RECOGOUT>") : data.find("</RECOGOUT>") + len("</RECOGOUT>")]

                        #pprint.pprint(xml)

                        # <s></s> ---> [s][/s]
                        xml = xml.replace('<s>','[s]')
                        xml = xml.replace('</s>','[/s]')

                        dict_ = xmltodict.parse(xml) # raise ERR
                        common.log(json.dumps(dict_,indent=2))

                        for whypo in dict_['RECOGOUT']['SHYPO']['WHYPO']:
                            if whypo['@PHONE'] == 'silB':
                                continue
                            if whypo['@PHONE'] == 'silE':
                                continue
                            else:
                                input_word.append(whypo['@WORD']) # word type is <class 'str'>

                        # 言葉を判別してどうこうするコードをここに書く
                        pprint(input_word)
                        for w in input_word:
                            common.log(w)
                            event.callSpeachRecog()
                            #event.publishSpeachRecog(w)
                    except ExpatError as err:
                        common.log("ErrorCode    :", errors.messages[err.code])
                        common.log("ErrorLineNum :", errors.messages[err.lineno])

                    data = ""
                else:
                    pass # 録音が一段落するまではなにも処理しないことを明示


def main():
    with JuliusController() as julius_controll:
        try:
            state = 0
            while True:
                if state == 0:
                    state = julius_controll.operate()
                elif state == 1:
                    ''' たまにJuliusが動かなくなる時があるので、その時はしばらく待って再び起動してみる '''
                    time.sleep(10)
                    julius_controll.reboot()
                    state = 0

        except KeyboardInterrupt:
            return


#common.thread_create( name=os.path.basename(__file__) + " main", target=main)
#main()
t_name = os.path.basename(__file__) + " : Julius"
thread = threading.Thread(target=main, name=t_name)
thread.setDaemon(True)
thread.start()
if __name__=="__main__":
    time.sleep(60) # for debug

