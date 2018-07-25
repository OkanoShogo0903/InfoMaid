## 何のプログラムかをメモ
- main
[x] main.py

- 共通部分
	- 音声出力
	[x] audio.py
	[ ] filer.py
	[ ] jtalk.py
	- センサー
	[ ] senser.py ---> pub
	- イベントを扱うところ
	[ ] event_master
	- 自然言語処理
	[ ] 	---> pub

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
[ ] 音声キュー、audioとjtalkの親
jtalkはaudioに統合する
