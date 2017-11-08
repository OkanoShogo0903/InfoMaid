import sys
#sys.path.append("C:\\Users\\okano\\Anaconda3\\Lib\\site-packages")
# C:\Users\okano\Anaconda3\Lib\site-packages
from datetime import datetime
import locale
import wave
import pyaudio
import time
import threading
import random
import os

import jtalk
import filer

AUDIO_URL = "../etcs/Audio/"

a = datetime.now()

def audio_func(url):
    wavfile = url

    # WAVファイルを開く
    wf = wave.open(wavfile, "rb")

    # PyAudioのインスタンスを生成 (1)
    p = pyaudio.PyAudio()

    # 再生用のコールバック関数を定義 (2)
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # Streamを生成(3)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    # Streamをつかって再生開始 (4)
    stream.start_stream()

    # 再生中はひとまず待っておきます (5)
    while stream.is_active():
        time.sleep(0.1)

    # 再生が終わると、ストリームを停止・解放 (6)
    stream.stop_stream()
    stream.close()
    wf.close()

    # close PyAudio (7)
    p.terminate()

def voice_timer():
    global a
    b = datetime.now()
    # 実質使われるのは10,20,30,40,50のデータのみ
    # 10 分ごとの時報
    if(b.minute%10 == 0):
    # TODO wavファイルがないときは例外を投げる
        audio_func( AUDIO_URL + "Init/master.wav")
        say_text = str(b.hour%12) + '時' + str(b.minute) + "分です"
        jtalk.jtalk(say_text)
    else:
    # なにもない時のリアクション
        # 1 ~ 100 の整数値をランダムに生成
        rand_int = random.randint(1,100)
        if 1 <= b.hour and b.hour <=4 :
            # 真夜中の場合の一般リアクション
            # 0を割り算するとエラーが起こる可能性を考慮 
            if (rand_int % 3 == 0): 
                url = AUDIO_URL + "other/midnight"
                url = filer.GetFileName(url)
                audio_func(url)
        elif 18 <= b.hour :
            # 夕方から夜にかけての場合の一般リアクション
            if (rand_int % 5 == 0):
                url = AUDIO_URL + "other/evening"
                url = filer.GetFileName(url)
                audio_func(url)
        elif 5 <= b.hour and b.hour <= 9 :
            # 朝の場合の一般リアクション
            if (rand_int % 5 == 0):
                url = AUDIO_URL + "other/morning"
                url = filer.GetFileName(url)
                audio_func(url)
        else:
            # 昼の場合の一般リアクション
            if (rand_int % 6 == 0):
                url = AUDIO_URL + "other/daytime"
                url = filer.GetFileName(url)
                audio_func(url)
    # 呼び出された後の処理
    a = datetime.now()
    # 指定秒に呼び出されるようにスレッドをセットする
    t=threading.Timer(60,voice_timer)
    t.start()

# main function
def main():
    print ("boice timer active")
    print (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print (os.getcwd())
    print ("\n")

    url = AUDIO_URL + "Init/init_voice.wav"
    audio_func(url)

    b = datetime.now()
    say_text = str(b.hour%12) + '時' + str(b.minute) + "分です"
    jtalk.jtalk(say_text)

    t=threading.Timer(1,voice_timer)
    t.start()

if __name__=="__main__":
    main()
