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

print ("boice timer active")
print (datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
print ("\n")

audio_url = "./etcs/Audio/"

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
    if(b.minute%10 == 0):
    # 10 分ごとの時報
    # TODO wavファイルがないときは例外を投げる
        audio_func( audio_url + "Init/master.wav")
        h_url = audio_url + str(b.hour%12) + "zi.wav"
        audio_func(h_url)
        m_url = audio_url + str(b.minute) + "m.wav"
        audio_func(m_url)
    else:
    # なにもない時のリアクション
        # 1 ~ 100 の整数値をランダムに生成
        rand_int = random.randint(1,100)
        if 1 < b.hour and b.hour < 5 : # b.hour が0~24の時のプログラム
            # 夜の場合の一般リアクション
            if (rand_int % 3 == 0): # 0を割り算するとエラーが起こる可能性を考慮
                url = audio_url + "other/yoru" + str(random.randint(1,3)) + ".wav"
                audio_func(url)
        else:
            # 昼の場合の一般リアクション
            if (rand_int % 5 == 0):
                #url = audio_url + "other/hiru" + str(random.randint(1,1)) + ".wav"
                #audio_func(url)
    # 呼び出された後の処理
    print ("h:" + b.hour + " m:" + b.minute + " s:" + b.second)
    a = datetime.now()
    # 指定秒に呼び出されるようにスレッドをセットする
    t=threading.Timer(60,voice_timer)
    t.start()
# main function
# TODO カレントディレクトリの問題か？
print(os.getcwd())
# absolute_file_path =
url = audio_url + "Init/init_voice.wav"
audio_func(url)

t=threading.Timer(1,voice_timer)
t.start()
