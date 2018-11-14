import snowboydecoder
def detectedCB():
    print "hotword detected"

AUDIO_URL = "../etcs/snowboy/"
detector = snowboydecoder.HotwordDetector("ヤッホー.pmdl", sensitivity=0.5, audio_gain=1)
detector.start(detectedCB)

