# InfoMaid
情報の面からメイドさん創作に対するアプローチを行う
  
* 天気やニュース情報の提供
* SNSのメンションやタイムラインの通知及び読み上げ
* 朝起こしてくれる
* 独り言をしゃべる
* ワードについて検索する
とかそんな感じの機能いろいろ

あと、メモとしてdoc.mdにも少し書いてある

## TODO 
* 音声が重なって再生される問題を解決する。mutexとかsubprocessの機能とかを探す。ボイロとは別件。  
 > 追記(2017-11-14):subprocess.Popen()だとプロセスを呼び出し終わる前に次の処理に移ってしまうため、subprocess.call()を使うことが望ましいと思われるため修正

* あまりうまく読み上げられていない。ボイロで解決？

* [みくみくまうす](http://mikumikumouth.net/)の調査  「読み上げテキストを解析して自動アニメーション」「読み上げ中のテキストを字幕表示」
  動作環境 Windows 7/8/8.1/10 32/64bit ---> 死亡

* ソースコード部分の表示はQiitaではもっとかっこよく背景青っぽくなっているので、それにしたい
* センサをどのピンに繋いでいるかを写真でとりたい
------------
# RaspberryPi SetUp
* Internet Activate 
~~~
$ vi /etc/dhcpd.conf
~~~
before
~~~
# Example static IP configuration:
#interface eth0
#static ip_address=192.168.0.10/24
#static ip6_address=fd51:42f8:caae:d92e::ff/64
#static routers=192.168.0.1
#static domain_name_servers=192.168.0.1 8.8.8.8 fd51:42f8:caae:d92e::1
~~~
after
~~~
# Example static IP configuration:
interface eth0static ip_address=172.16.158.41/16
static routers=172.16.0.1
static domain_name_servers=210.196.228.210 210.196.3.183
~~~
**After etc/dhcpd.conf edit,you should reboot**
* JapaseneKey
~~~
$ sudo apt-get install ibus-anthy
~~~
* Vim
$ sudo apt-get install vim
* Git
~~~
$ sudo apt-get install git
$ git config --global alias.graph "log --graph --date-order --all --pretty=format:'%h %Cred%d %Cgreen%ad %Cblue%cn %Creset%s' --date=short"
~~~
* Miniconda
[download Miniconda Python3.x for **ARM**](https://raspberrypi.stackexchange.com/questions/45663/which-miniconda-version-should-i-use-with-raspberry-pi-3)  
~~~
$ bash Miniconda3-latest-Linux-armv7l.sh
~~~
## Miniconda Hot Reference
It is Miniconda's command 

* Export : 
~~~
$ conda env export > (EXPORT_NAME).yaml
~~~
* Inport : 
~~~
$ conda env create -f (EXPORT_NAME).yaml
~~~
* Deleat :
~~~
$ conda env remove -n (EXPORT_NAME)
~~~

## Library Install
TODO
pyaduioはこのportaudioを入れなければ聞かない可能性もあるので、
この欄の扱いは保留
*pyaudio* is cannot install by normal pip
~~~
$ sudo apt-get install portaudio19-dev
$ pip install pyaudio
~~~
------------
## OpenJtalk Install
[参考にしたサイト](http://shokai.org/blog/archives/6893)  
~~~
$ sudo apt-get install open-jtalk open-jtalk-mecab-naist-jdic htsengine libhtsengine-dev hts-voice-nitech-jp-atr503-m001
~~~

## OpenJTalk VoiceData Setting
**Using OpenJTalk version handle hts-voice.**  
**Do not use Mei's voice files.**  
Your OpenJtalk version is not support Mei's voice file  
~~~
$ sudo cp -r InfoMaid/etcs/Miku_A/ /usr/share/hts-voice/
~~~
------------
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

# オーディオモジュールの設定
## 優先順位の確認
以下のコマンドで確認できる。  
名前の前に出てくる数字が優先順位で、snd_usb_audioを最優先にしたい。  
おそらく、初めは以下のようにUSBマイクの方が優先順位が低くなっている。
~~~
$ cat /proc/asound/modules
 0 snd_bcm2835
 1 snd_usb_audio
~~~

## 優先順位の書き換え
下記のように設定を変更する。  
この**alsa_base.confが存在しない場合は、新しく作る**。ソースは[ここ](https://qiita.com/kinpira/items/75513eaab6eed19da9a3)。
~~~
$ vi /etc/modprobe.d/alsa-base.conf
options snd slots=snd_usb_audio,snd_bcm2835
options snd_usb_audio index=0
options snd_bcm2835 index=1
~~~

## 再度、優先順位の確認
一度**再起動**してから、再度オーディオモジュールの優先順位を確認する。
~~~
$ cat /proc/asound/modules
 0 snd_usb_audio
 1 snd_bcm2835
~~~
こんな風に優先順位が変わっているはず

# マイクの設定
[参考にしたサイト](https://qiita.com/t_oginogin/items/f0ba9d2eb622c05558f4)
## マイクの音量調整
-c 0ではさっき調べたカード番号を入れます。
40というのはボリュームで、0から62を入れれます。
~~~
$ amixer sset Mic 40 -c 0
~~~

## マイクが生きているかを確かめる
~~~
$ speaker-test -t sine -f 600
~~~
## マイクのカード番号、デバイス番号を確認
この場合はカード:0のデバイス:0を使えばいい
~~~
$ arecord -l
**** ハードウェアデバイス CAPTURE のリスト ****
カード 0: Microphone [USB Microphone], デバイス 0: USB Audio [USB Audio]
  サブデバイス: 1/1
  サブデバイス #0: subdevice #0
~~~

## 録音
0,0でカード,デバイスを指定しています。
~~~
$ arecord -D plughw:0,0 test.wav
~~~
## 録音したものを再生する
~~~
aplay test.wav
~~~
ここまでうまくいけば、マイクの設定はOK
## うまく再生されなかったとき
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
上記のコマンドから分かったカード番号とデバイス番号を使って、
~~~
$ aplay -Dhw:1,0 test.wav
~~~
# Julius
Juliusについての説明・注意事項
* **ここではv4.3.1をダウンロードしているが、ウェブの情報はv4.2.3が多い。 
違うヴァージョンの記事では起動すら危ういので注意**
* **grammar-kit-v4.1 及び julius-4.3.1/gramtools/mkdfa/ に付属している mkdfa.pl（から参照されるmkfa） は正常に動作しないので、julius ディレクトリ内にある対応版の mkfa を利用する必要がある。**
* Julius4からJulianと統合された。
* Juliusは言語モデルと音響モデルから最尤を出すエンジンなので、識精度は使用するモデルによって大きく変化する。
(Juliusが日常会話で認識精度が低いのは、Julius標準のモデルの問題)
* Julius-4.4より音響モデルでDNN-HMMを使用可能。
* 言語モデルはNNを未サポート。
* モジュールモードで動かせばTCP/IPで通信できる。

## Install
* [Julius](http://julius.osdn.jp/)のソースコードからコンパイル
~~~
$ cd
$ wget --trust-server-names 'http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F60273%2Fjulius-4.3.1.tar.gz'
$ tar xvzf julius-4.3.1.tar.gz
$ cd julius-4.3.1/
$ ./configure
$ make
#$ sudo make install
~~~
* ディクテーションファイル
~~~
$ mkdir ~/julius-kits
$ cd ~/julius-kits
$ wget --trust-server-names 'http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F60416%2Fdictation-kit-v4.3.1-linux.tgz'
$ tar xvzf dictation-kit-v4.3.1-linux.tgz
~~~
* Juliusの実行
plughw:0,0はマイクのカードとデバイスの番号に合わせる
~~~
$ ALSADEV="plughw:0,0" ~/julius-4.3.1/julius/julius -C ~/julius-kits/dictation-kit-v4.3.1-linux/main.jconf -C ~/julius-kits/dictation-kit-v4.3.1-linux/am-gmm.jconf -nostrip
~~~
* 起動時のオプション
[リファレンス・マニュアル(公式)](https://julius.osdn.jp/juliusbook/ja/julius.html)

## Juliusについてのメモ
ファイルの役割について  
Juliusはjulianが後から統合された流れもあってか、ファイル構成が複雑  
* grammar-kit-4.3.1
	文法
* julius-4.3.1
	julius本体、ソースコードからコンパイルしたもの
* julius-kits --- dictation-kit-v4.3.1-linux
	音声認識用モデル
* *.grammar : 文法規則  
* *.voca : 語彙辞書  

* 音響モデル
	HMM(隠れ,マルコフ,モデル)が主流で、JuliusでもHMMに対応している。  
	うまく音声認識をさせたいのならば、話者の性別や癖、喋っている場所が室内であるか屋外であるかなどの音響的特徴を反映した音響モデルが有償で販売されている。  
	自分で音響モデルを作るためのツールキットにHTKというものがあるが、言語モデル以上に膨大な専門的知識が必要になるのでオススメできない。  
	* [Kaldi](https://qiita.com/nina_rumor/items/f5aca2aea404a0f19fd1)(カルディ)
		C++で書かれたツールキット  
		日本語のドキュメントがない  
		NNを使える音声認識ツールキット。
	* CSJ
		日本語話し言葉コーパス( Corpus of Spontaneous Japanese : CSJ )  
		国立機関が日本語の発音を大量に集めた研究用のデータベースで、利用には申請が必要。  
		学術研究飲みの場合、研究機関50k、学生2.5k。  
* 言語モデル
	単語辞書と単語間の接続によって、接続された単語の音を示す。  
	* SRILM
		N-gram言語モデルの自作ツール。これは公開されており、学校機関なら無償利用できる。
* [辞書について](http://feijoa.jp/laboratory/raspberrypi/julius442/)
* コマンド例
~~~
julius -C main.jconf -C am-gmm.jconf -demo
julius -C ~/grammar-kit-4.3.1/hmm_mono.jconf -input mic -gram kaden -nostrip

動かない
ALSADEV="plughw:1,0" julius -C ~/grammar-kit-4.3.1/hmm_mono.jconf -gram greeting -nostrip 

動く
ALSADEV="plughw:1,0" julius -C ~/julius-kits/dictation-kit-v4.3.1-linux/main.jconf -C ~/julius-kits/dictation-kit-v4.3.1-linux/am-gmm.jconf -nostrip

~~~

## Juliusの評価
いやこのコンパイラはいかれてるでしょ。
READMEの指示通りにやってもエラー吐きます。
README読んだじゃん！README読んだじゃん！

------------
# Sencer
## MotionSencer
GPIO17のピン番号は11なので注意  

|vcc|ground|out|
|:-:|:-:|:-:|
|  01  |  06  |  11  |

------------
# Using
