## 何のプログラムか
- main
[x] main.py
[x] common_function

- 共通部分
	- 音声出力
	[x] audio.py
	[x] filer.py
	[x] jtalk.py
	- センサー
	[x] senser.py ---> pub
	- イベントを扱うところ
	[x] event_master
	- 自然言語処理
	[x] nlp ---> pub

- 要素技術(class化する)
	- Julius
	[x] move_julius.py ---> pub
	- 時報、日報
	[x] clock_func.py <--- sub(speech)
	[x] day_list.py
	- 天気
	[x] weather.py <--- sub(speech,senser)
	- ニュース
	[ ] news.py <--- sub(speech,senser)
	[ ] beautiful_soup.py
	[ ] rss.py
	[ ] site_list.py
	- ツイッター
	[ ] tweet.py <--- sub(speech)
	[ ] geophysics.py

- other
[ ] web_search.py
[x] AudioQueueの実装(audioとjtalkの親)
[ ]	jtalkはaudioに統合する
[ ] main.pyは<C-c>で落ちるようにして、他のスレッドはすべてデーモンにしてプログラム全体が<C-c>一発で落ちるようにする.

# メモ
- while1で回すと処理が重くなるから、スレッド処理で軽くしてあげたほうがいい？
