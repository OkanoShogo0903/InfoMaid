import feedparser
from datetime import datetime
from time import mktime
def Rss():
    #RSSのURL
    RSS_URL  = "https://news.yahoo.co.jp/pickup/economy/rss.xml"
#    RSS_URL  = "http://www.japantoday.com/feed/"

    #RSSの取得
    feed = feedparser.parse(RSS_URL)

    #RSSのタイトル
    print (feed.feed.title)
    
    news_list = []
    for entry in range(len(feed.entries)):
        #RSSの内容を一件づつ処理する
        title = feed.entries[entry].title
        link = feed.entries[entry].link

        #更新日を文字列として取得
        published_string = feed.entries[entry].published

        #更新日をdatetimeとして取得
        tmp = feed.entries[entry].published_parsed
        published_datetime = datetime.fromtimestamp(mktime(tmp))

        #表示
        print (title)
        print (link)
        print (published_string)
        print (published_datetime)

        # 新しく追加する辞書を構成する
        dict_ = {}
        dict_ = {"title":"","text":"","genre":"","link":""}
        dict_["title"] = title
        dict_["link"] = link
        news_list.append(dict_)

    # 入手したデータを画面に出力
    for tmp in news_list:
        print("title:" + tmp["title"])
        print("genre:" + tmp["genre"])
        print("link :" + tmp["link"])
        print("text :" + tmp["text"])
 
if __name__=="__main__":
    Rss()
