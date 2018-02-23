# InfoMaid
情報の面からメイドさん創作に対するアプローチを行う
  
* 天気やニュース情報の提供
* SNSのメンションやタイムラインの通知及び読み上げ
* 朝起こしてくれる
* 独り言をしゃべる
* ワードについて検索する
とかそんな感じの機能いろいろ

## TODO 
* 音声が重なって再生される問題を解決する。mutexとかsubprocessの機能とかを探す。ボイロとは別件。  
 > 追記(2017-11-14):subprocess.Popen()だとプロセスを呼び出し終わる前に次の処理に移ってしまうため、subprocess.call()を使うことが望ましいと思われるため修正

* あまりうまく読み上げられていない。ボイロで解決？

* [みくみくまうす](http://mikumikumouth.net/)の調査  「読み上げテキストを解析して自動アニメーション」「読み上げ中のテキストを字幕表示」
  動作環境 Windows 7/8/8.1/10 32/64bit ---> 死亡

* ソースコード部分の表示はQiitaではもっとかっこよく背景青っぽくなっているので、それにしたい
------------
# Install
## Miniconda
It is Miniconda's command 
* export : 
~~~
$ conda env export > (export_name).yaml
~~~
* inport : 
~~~
$ conda env create -f (export_name).yaml
~~~
* deleat:
~~~
$ conda env remove -n ENVIRONMENT
~~~

## Library Install
* pyaudio
* twitter
~~~
$ sudo apt-get install portaudio19-dev
$ pip install pyaudio

$ pip install python-twitter
~~~

## OpenJtalk Install
[参考にしたサイト](http://shokai.org/blog/archives/6893)  
~~~
$ sudo apt-get install open-jtalk open-jtalk-mecab-naist-jdic htsengine libhtsengine-dev hts-voice-nitech-jp-atr503-m001
~~~

## OpenJTalk VoiceData Setting
Using OpenJTalk version handle hts-voice.  
**Do not use mei's voice files**  
  
It is test code
~~~
$ cp ./etcs/Miku_A/ /usr/share/hts-voice/
~~~

## ライブラリのインストール
~~~
$ sudo apt-get install alsa-utils sox libsox-fmt-all
~~~
## USBポートの確認
~~~
$ lsusb
Bus 001 Device 006: ID 0d8c:0016 C-Media Electronics, Inc. 
Bus 001 Device 005: ID 413c:2105 Dell Computer Corp. Model L100 Keyboard
Bus 001 Device 004: ID 413c:3012 Dell Computer Corp. Optical Wheel Mouse
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. SMSC9512/9514 Fast Ethernet Adapter
Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. SMC9514 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
~~~

## オーディオモジュールの設定
### 優先順位の確認
以下のコマンドで確認できる。  
名前の前に出てくる数字が優先順位で、snd_usb_audioを最優先にしたい。  
おそらく、初めは以下のようにUSBマイクの方が優先順位が低くなっている。
~~~
$ cat /proc/asound/modules
 0 snd_bcm2835
 1 snd_usb_audio
~~~

### 優先順位の書き換え
下記のように設定を変更する。  
この**alsa_base.confが存在しない場合は、新しく作る**。ソースは[ここ](https://qiita.com/kinpira/items/75513eaab6eed19da9a3)。
~~~
$ vi /etc/modprobe.d/alsa-base.conf
options snd slots=snd_usb_audio,snd_bcm2835
options snd_usb_audio index=0
options snd_bcm2835 index=1
~~~

### 再度、優先順位の確認
一度**再起動**してから、再度オーディオモジュールの優先順位を確認する。
~~~
$ cat /proc/asound/modules
 0 snd_usb_audio
 1 snd_bcm2835
~~~
こんな風に優先順位が変わっているはず

## マイクの設定
[参考にしたサイト](https://qiita.com/t_oginogin/items/f0ba9d2eb622c05558f4)
### マイクのカード番号を確認
~~~
$ arecord -l
**** ハードウェアデバイス CAPTURE のリスト ****
カード 0: Microphone [USB Microphone], デバイス 0: USB Audio [USB Audio]
  サブデバイス: 1/1
  サブデバイス #0: subdevice #0
~~~

### マイクの音量調整
マイクのボリュームの設定コマンドです。  
 ~~~ -c 0 ~~~ ではさっき調べたカード番号を入れます。
ここで使っている ~~~ 40 ~~~ というのはボリュームで、最小0で最大は62です。
~~~
$ amixer sset Mic 40 -c 0
~~~

### マイクが生きているかを確かめる
~~~
$ speaker-test -t sine -f 600
~~~

### マイクで録音してみる(動作の確認)
以下のコマンドで、カード:0のデバイス:0を使えばいいことが分かります。
~~~
$ arecord -l
**** ハードウェアデバイス CAPTURE のリスト ****
カード 0: Microphone [USB Microphone], デバイス 0: USB Audio [USB Audio]
  サブデバイス: 1/1
  サブデバイス #0: subdevice #0
~~~
この ~~~ 0,0 ~~~ でカード,デバイスを指定してます。
~~~
$ arecord -D plughw:0,0 test.wav
~~~
### 録音したものを再生する
~~~
aplay test.wav
~~~
#### うまく再生されなかったとき
以下のコマンドで、デバイスを確認します。  
カード:1のデバイス:1はHDMIなので、これは違うようです。  
カード:1のデバイス:0を使えばいいことが分かります。
~~~
$ aplay -l
**** ハードウェアデバイス PLAYBACK のリスト ****
カード 1: ALSA [bcm2835 ALSA], デバイス 0: bcm2835 ALSA [bcm2835 ALSA]
    サブデバイス: 8/8
    サブデバイス #0: subdevice #0
    サブデバイス #1: subdevice #1
    サブデバイス #2: subdevice #2
    サブデバイス #3: subdevice #3
    サブデバイス #4: subdevice #4
    サブデバイス #5: subdevice #5
    サブデバイス #6: subdevice #6
    サブデバイス #7: subdevice #7
カード 1: ALSA [bcm2835 ALSA], デバイス 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]
    サブデバイス: 1/1
    サブデバイス #0: subdevice #0
~~~
そして、上記のコマンドから分かったカードとデバイスを使って、
~~~
$ aplay -Dhw:1,0 test.wav
~~~
## Julius
### Install
* [Julius](http://julius.osdn.jp/)のソースコードからコンパイル
~~~
$ wget --trust-server-names 'http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F60273%2Fjulius-4.3.1.tar.gz'
$ tar xvzf julius-4.3.1.tar.gz
$ cd julius-4.3.1/
$ ./configure
$ make
~~~
* ディクテーションファイル
~~~
$ mkdir ~/julius-kits
$ cd ~/julius-kits
$ wget --trust-server-names 'http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F60416%2Fdictation-kit-v4.3.1-linux.tgz'
$ tar xvzf dictation-kit-v4.3.1-linux.tgz
~~~
* Juliusの実行(plughw:0,0はマイクのカードとデバイスの番号)
~~~
$ ALSADEV="plughw:0,0" ~/julius-4.3.1/julius/julius -C ~/julius-kits/dictation-kit-v4.3.1-linux/main.jconf -C ~/julius-kits/dictation-kit-v4.3.1-linux/am-gmm.jconf -nostrip
~~~
------------
# Using
