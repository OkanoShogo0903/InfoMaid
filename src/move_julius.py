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
#import xml.etree.ElementTree as ET

import xmltodict
from xml.parsers.expat import ExpatError,errors
import json

HOST = 'localhost'
PORT = 10500
BUFSIZE = 4096

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
    # Juliusの起動スクリプトを実行する
    #activate_command = "ALSADEV=\"plughw:1,0\" julius -C ~/grammar-kit-4.3.1/testmic.jconf -gram ~/dict/greeting -nostrip -module"
    #activate_command = ["ALSADEV=\"plughw:1,0\"","julius","-C","~/grammar-kit-4.3.1/testmic.jconf","-gram","~/dict/greeting","-nostrip","-module"]

    #print(activate_command)
    #command('sh start_julius.sh')
    #command(activate_command)
    #sleep(3)
#    invoke_julius()

    # ソケット通信の接続を行う
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # TCPサーバー接続の初期化
        client.connect((HOST,PORT))
    except:
        print("ERRER :ソケット接続のエラーが発生したため終了します")
        sys.exit(0)

    # ソケット接続に関連した文書を作成する。
    sf = client.makefile('rb')

    try:
        # サーバからのデータ受信
        print("データ受信を開始します")
        data = ""
        while 1:
            # print(client.recv(BUFSIZE)) # test
            # data = data + client.recv(BUFSIZE)
            data = data + str(client.recv(BUFSIZE))
            # TCPデータを受信するまで待機し、受信データを文字列として返す
#            print("client : ",data)

            if "INPUT" in data:
                print("インプットってはいってたよ")

            #if "</RECOGOUT>\n." in data: TODO \n.省略したらifの中に入るようになったけど、これで本当に大丈夫か？
            if "</RECOGOUT>" in data:
                print("録音終了したので、一旦クリア！！")
                # RECOGOUT要素以下をXMLとしてパース
                # root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("\n.", ""))
                # 現状ここで起こるエラーは\nを認識できていないためなので、文字コードとかを確認してutf-8にエンコードして、ここでのエラーが消えるかを見る
                # \\nを消したらxmlパーサ通った
                # xml = '<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):]
                try:
                    xml = data[data.find("<RECOGOUT>"):]
                    xml = xml.replace("\\n.\\n\'","") # \nを消さないとxmlからパースできないため
                    xml = xml.replace("\\n","")
                    xml = xml.replace("'b'","")
                    
                    # print(xml.encode('uft-8'))
                    print(xml)

                    dict_ = xmltodict.parse(xml)
                    print(json.dumps(dict_,indent=2))
                    for whypo in dict_['RECOGOUT']['SHYPO']['WHYPO']:
                        if whypo['@PHONE'] == 'silB':
                            print("***")
                            continue
                        if whypo['@PHONE'] == 'silE':
                            print("***")
                            continue
                        import types
                        print(type(whypo))
                        print(whypo)
                        print(type(whypo['@WORD']))
                        print(whypo['@WORD']) # \xe3\x81\x8a\xe3\x81\xaf\xe3\x82\x88\xe3\x81\x86とか入る
                        # TODO ここでの@WORDの文字コード問題
                        #print(whypo['@WORD'].decode('utf-8'))
                        #print(whypo['@WORD'].replace("\\\\","\\").decode('utf-8'))

                    """
                    <RECOGOUT>\n  <SHYPO RANK="1" SCORE="-2302.836426" GRAM="0">\n    <WHYPO WORD="[s]" CLASSID="4" PHONE="silB" CM="1.000"/>\n    <WHYPO WORD="\xe3\x81\x8a\xe3\x81\xaf\xe3\x82\x88\xe3\x81\x86" CLASSID="0" PHONE="o h a y o u" CM="0.902"/>\n    <WHYPO WORD="[/s]" CLASSID="5" PHONE="silE" CM="0.755"/>\n  </SHYPO>\n</RECOGOUT>\n.\n'
                    """
                    """
                    # どうも[s]の場合と<s>の場合があって、<s>は通らないらしい
                    <RECOGOUT>  <SHYPO RANK="1" SCORE="-1886.061279" GRAM="1">    <WHYPO WORD="<s>" CLASSID="7" PHONE="silB" CM="1.000"/>    <WHYPO WORD="\x82\xd4\x82\xc7\x82\xa4" CLASSID="0" PHONE="b u d o:" CM="0.614"/>    <WHYPO WORD="\x82\xc5\x82\xb7" CLASSID="6" PHONE="d e s u" CM="1.000"/>    <WHYPO WORD="</s>" CLASSID="8" PHONE="silE" CM="0.976"/>  </SHYPO></RECOGOUT>
                    """
                    """
                    # 根本的な理由は、juliusから渡されるデータがutf-8にエンコードされていないと言うことなので、
                    # 次回からjuliusをプログラム上から起動する方法を試していくことにする
                    """

                except ExpatError as err:
                    print("ErrorCode    :", errors.messages[err.code])
                    print("ErrorLineNum :", errors.messages[err.lineno])

                # 言葉を判別してどうこうするコードをここに書く
                data = ""

    except KeyboardInterrupt:
        # Ctrl+Cとか押されたとき
        print("keyInterrupt Occured.")
        # TODO juliusのプロセス終了
        # julius にkillコマンドを送る(web情報では、killによって終了しないjuliusのバグがあるらしい)
        client.close
        sys.exit(0)

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
    main()

