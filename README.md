# InfoMaid
情報の面からメイドさん創作に対するアプローチを行う
  
* 天気やニュース情報の提供
* SNSのメンションやタイムラインの通知及び読み上げ
* 朝起こしてくれる
* 独り言をしゃべる
* ワードについて検索する
とかそんな感じの機能いろいろ

### TODO 
* 音声が重なって再生される問題を解決する。mutexとかsubprocessの機能とかを探す。ボイロとは別件。  
 > 追記(2017-11-14):subprocess.Popen()だとプロセスを呼び出し終わる前に次の処理に移ってしまうため、subprocess.call()を使うことが望ましいと思われるため修正

* あまりうまく読み上げられていない。ボイロで解決？

* [みくみくまうす](http://mikumikumouth.net/)の調査  「読み上げテキストを解析して自動アニメーション」「読み上げ中のテキストを字幕表示」
  動作環境 Windows 7/8/8.1/10 32/64bit ---> 死亡

------------
# Install
### Miniconda
It is Miniconda's command 
* export : 
~~~
conda env export > (export_name).yaml
~~~
* inport : 
~~~
conda env create -f (export_name).yaml
~~~
* deleat:
~~~
conda env remove -n ENVIRONMENT
~~~

### Library Install
* pyaudio
* twitter
~~~
sudo apt-get install portaudio19-dev
pip install pyaudio

pip install python-twitter
~~~

### OpenJtalk Install
[参考にしたサイト](http://shokai.org/blog/archives/6893)  
~~~
sudo apt-get install open-jtalk open-jtalk-mecab-naist-jdic htsengine libhtsengine-dev hts-voice-nitech-jp-atr503-m001
~~~

### OpenJTalk VoiceData Setting
Using OpenJTalk version handle hts-voice.  
**Do not use mei's voice files**  
  
It is test code
~~~
cp ./etcs/Miku_A/ /usr/share/hts-voice/
~~~

### Julius Install
[参考にしたサイト](https://qiita.com/t_oginogin/items/f0ba9d2eb622c05558f4)
#### ライブラリのインストール
~~~
$ sudo apt-get install alsa-utils sox libsox-fmt-all
~~~
#### USBポートの確認
~~~
$ lsusb
Bus 001 Device 006: ID 0d8c:0016 C-Media Electronics, Inc. 
Bus 001 Device 005: ID 413c:2105 Dell Computer Corp. Model L100 Keyboard
Bus 001 Device 004: ID 413c:3012 Dell Computer Corp. Optical Wheel Mouse
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. SMSC9512/9514 Fast Ethernet Adapter
Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. SMC9514 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
~~~
#### オーディオモジュールの優先順位の確認
~~~
$ cat /proc/asound/modules
 0 snd_bcm2835
 1 snd_usb_audio
~~~
名前の前に出てくる数字が優先順位で、snd_usb_audioを最優先にしたい。
~~~
$ vi /etc/modprobe.d/alsa-base.conf
options snd slots=snd_usb_audio,snd_bcm2835
options snd_usb_audio index=0
options snd_bcm2835 index=1
~~~
上記のように設定を変更する。このalsa_base.confが存在しない場合は、新しく作ってしまえばいい。ソースは[ここ](https://qiita.com/kinpira/items/75513eaab6eed19da9a3)。
変更したら一度リブートして、再度オーディオモジュールの優先順位を確認する。
~~~
$ cat /proc/asound/modules
 0 snd_usb_audio
 1 snd_bcm2835
~~~

#### マイクの音量調整
カード番号を確認します
~~~
$ arecord -l
**** ハードウェアデバイス CAPTURE のリスト ****
カード 0: Microphone [USB Microphone], デバイス 0: USB Audio [USB Audio]
サブデバイス: 1/1
サブデバイス #0: subdevice #0
~~~

マイクのボリュームの設定コマンドです。  
~~~-c 0~~~ではさっき調べたカード番号を入れます。
16というのはボリュームで、最大は62です。
~~~
$ amixer sset Mic 16 -c 0
~~~
------------
# Using
