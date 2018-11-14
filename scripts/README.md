## しんちょく
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
	[x] news.py <--- sub(speech,senser)
	[x] beautiful_soup.py
	[x] rss.py
	[x] site_list.py
	- ツイッター
	[ ] tweet.py <--- sub(speech)
	[x] geophysics.py

# やることリスト
[ ] web_search.py
[x] AudioQueueの実装(audioとjtalkの親)
[ ]	jtalkはaudioに統合する
[ ] main.pyは<C-c>で落ちるようにして、他のスレッドはすべてデーモンにしてプログラム全体が<C-c>一発で落ちるようにする.
[ ] ニュースの取得をサイトごとにマルチスレッドで並列で処理させて、起動を早くするか？？
[ ] システムウェイクアップフェイズに以降とか、起動フェイズ開始とか、そんな感じにバラエティーを持たせたい.
[ ] システム起動中はピロピロ音を鳴らすとかよくない???
[ ] オルガとか、特殊ワードに反応させたい.
[ ] 今日の天気しか言わないので、時間によっては明日の天気を言うようにしたい.

# メモ
- 音声認識中になんか音だす?
- C-cで落とすときにも音を鳴らす
- twitterデータの秘匿
- subprocessモジュールは引数でdaemon化できないっぽいので、daemonライブラリを調べる
- 句点、句読点を消す

# err or warning
- newsからjtalkに送ったところで発生?  
WARNING: JPCommonLabel_insert_word() in jpcommon_label.c: First mora should not be short pause.

- julius
  File "/home/pi/デスクトップ/InfoMaid/src/move_julius.py", line 58, in __del__
      while self.julius.poll() is None:
	  AttributeError: 'NoneType' object has no attribute 'poll'

- twitter
	原因はtwitterAPIの仕様変更のため???
	result = self.api.home_timeline()
	tweepy.error.RateLimitError: [{'code': 88, 'message': 'Rate limit exceeded'}]

