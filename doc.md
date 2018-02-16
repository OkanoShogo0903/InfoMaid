# 備忘録
## Tweepyについて
* result_typeを指定するとgeocodeを含む検索がエラーはでないが空撃ちになる謎仕様  
そもそもresult_type自体がTweepyのAPI仕様には載っていない?
OK
~~~
result = self.api.search(q=word, count=count, lang=lang)
result = self.api.search(q="geocode:~~~,~~~,~~km "+word, count=count, lang=lang)
result = self.api.search(q=word, count=count, lang=lang, geocode=geocode)
~~~
ERRER
~~~
result = self.api.search(q=word, count=count, lang=lang, result_type=result_type, geocode=geocode)
~~~
