import time
import wave
import pyaudio
def play(url):
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


