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

------------
# Using
