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

class Julius(object):
    def __init__(self, option):
        # Juliusを起動するためのシェルコマンド
        #args = r'ALSADEV=\"plughw:1,0\" /usr/local/bin/julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module'
        device = 'ALSADEV=\"plughw:0,0\"'
        julius_path = "julius"
        self.args = device + ' ' + julius_path + ' ' + option

        self.BUFSIZE = 4096
        self.julius = None
        self.julius_socket = None
        self.julius, self.julius_socket, self.sf = self.invokeJuliusSet()


    def __enter__(self):
        # withステートメントで処理するための記述
        return self

    def __exit__(self, type, value, traceback):
        common.log("__exit__ call")

    def __del__(self):
        common.log("__del__ call")
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
        p = subprocess.Popen(
                #shlex.split(args),
                self.args,
                stdin=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
        time.sleep(2.0) # Juliusの起動待ち
        #common.log('INFO : invoke julius complete')
        return p


    def invokeJuliusSet(self):
        common.log('INFO : invoke julius set')

        # プロセスの用意
        julius = self.invokeJulius()
        # ソケット通信の接続を行う
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            time.sleep(3) # <--- Important!!!
            # TCPサーバー接続の初期化
            s.connect(('localhost', 10500))
        except:
            common.log("ERRER :ソケット接続のエラーが発生したため終了します") # ERR 111
            import traceback
            traceback.print_exc()

            stdout_data, stderr_data = julius.communicate(timeout=5) # sec
            print("communicate out : ",stdout_data)
            print("communicate err : ",stderr_data)

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
                data = data + self.julius_socket.recv(self.BUFSIZE).decode('utf-8')
                #common.log('[utf-8 decode]')
            
            except UnicodeDecodeError:
                data = data + self.julius_socket.recv(BUFSIZE).decode('cp932')
                common.log('[cp932 decode]')

            except ConnectionResetError:
                common.log("ConnectionResetError")
                #sys.exit(0)
                return -1

            except:
                import traceback
                traceback.print_exc()
                return -1

            if "ERREXIT" in data:
                common.log("Juliusが異常終了しました.")
                common.log("コンピュータの再起動を推奨します.")
                sys.exit(data) # <---プログラムの終了
            else:
                #common.log("Julius active")
                pass

            #print("julius_socket START ************************************")
            #pprint.pprint(data)
            #print("julius_socket END   ************************************")

            #stdout_data, stderr_data = julius.communicate() # sec
            #print ("communicate out : ",stdout_data)
            #print ("communicate err : ",stderr_data)

            if self.julius.poll() is not None:   # means , julius dead
                common.log("Julius non active")
                self.deleteSocket(self.julius_socket)
                self.julius, self.julius_socket, self.sf = self.invokeJuliusSet()
            else:
                if "INPUT" in data:
                    pass # ---> 音声入力開始のイベントを出すのもよい

                if "</RECOGOUT>" in data:
                    input_word = []
                    # 録音が一段落したので、処理開始--->
                    try:
                        # xmlパーサにかけるために、必要な部分を抽出する
                        xml = data[data.rfind("<RECOGOUT>") : data.find("</RECOGOUT>") + len("</RECOGOUT>")]

                        # <s></s> ---> [s][/s]
                        xml = xml.replace('<s>','[s]')
                        xml = xml.replace('</s>','[/s]')

                        dict_ = xmltodict.parse(xml) # raise ERR
                        common.log(json.dumps(dict_,indent=2))

                        try:
                            for whypo in dict_['RECOGOUT']['SHYPO']['WHYPO']:
                                if whypo['@PHONE'] == 'silB':
                                    continue
                                elif whypo['@PHONE'] == 'silE':
                                    continue
                                else:
                                    input_word.append(whypo['@WORD']) # word type is <class 'str'>

                        except TypeError:
                            whypo = dict_['RECOGOUT']['SHYPO']['WHYPO']
                            input_word.append(whypo['@WORD'])
                        except:
                            import traceback
                            traceback.print_exc()
                            sys.exit()

                        # 言葉を判別してどうこうするコードをここに書く
                        for w in input_word:
                            common.log(w)
                            #event.callSpeechRecog()
                            event.publishSpeechRecog(w)

                    except ExpatError as err:
                        common.log("ErrorCode    :", errors.messages[err.code])
                        common.log("ErrorLineNum :", errors.messages[err.lineno])
                    except:
                        import traceback
                        traceback.print_exc()

                    data = ""
                else:
                    pass # 録音が一段落するまではなにも処理しないことを明示


class JuliusControllerDailyWord(Julius):
    options = "\
            -d     ~/julius-kits/dictation-kit-v4.3.1-linux/model/lang_m/bccwj.60k.bingram\
            -v     ~/julius-kits/dictation-kit-v4.3.1-linux/model/lang_m/bccwj.60k.htkdic\
            -h     ~/julius-kits/dictation-kit-v4.3.1-linux/model/phone_m/jnas-tri-3k16-gid.binhmm\
            -hlist ~/julius-kits/dictation-kit-v4.3.1-linux/model/phone_m/logicalTri\
            -lmp 8.0 -2.0\
            -lmp2 8.0 -2.0\
            -b 1500\
            -b2 100\
            -s 500\
            -m 10000\
            -n 30\
            -output 1\
            -zmeanframe\
            -rejectshort 200\
            -input mic\
            -module\
            "
    def __init__(self):
        super().__init__(self.options)
        #dictation_options = "\
        #        -C ~/julius-kits/dictation-kit-v4.3.1-linux/main.jconf\
        #        -C ~/julius-kits/dictation-kit-v4.3.1-linux/am-gmm.jconf\
        #        -module\
        #        "


class JuliusControllerDictation(Julius):
    options = "\
            -w     ~/julius-kits/dictation-kit-v4.3.1-linux/d.dic\
            -v     ~/julius-kits/dictation-kit-v4.3.1-linux/model/lang_m/bccwj.60k.htkdic\
            -h     ~/julius-kits/dictation-kit-v4.3.1-linux/model/phone_m/jnas-tri-3k16-gid.binhmm\
            -hlist ~/julius-kits/dictation-kit-v4.3.1-linux/model/phone_m/logicalTri\
            -n 5\
            -input mic\
            -zmeanframe\
            -charconv euc-jp utf8 \
            -nostrip\
            -module\
            "
    def __init__(self):
        super().__init__(self.options)


def main():
    with JuliusControllerDictation() as julius_controll:
    #with JuliusControllerDailyWord() as julius_controll:
        try:
            state = 0
            while True:
                if state == 0:
                    state = julius_controll.operate()
                elif state == -1:
                    '''
                        たまにJuliusが動かなくなる時があるので、その時はしばらく待って再び起動してみる
                    '''
                    common.log("Juliusの正常起動へ復帰を試みます******************")
                    time.sleep(5) # 10で正常に復帰することを確認
                    julius_controll.reboot()
                    state = 0

        except KeyboardInterrupt:
            sys.exit(0)
            return


#common.thread_create( name=os.path.basename(__file__) + " main", target=main)
#main()
threading.Thread(\
        target=main,\
        name="Julius",\
        daemon=True\
        ).start()

if __name__=="__main__":
    time.sleep(60) # for debug

