import feedparser
from datetime import datetime
from time import mktime
def RssMahter():
# 音声でジャンルを指定したり、ランダムなジャンルからニュースを取得したり、時間帯によって取得するジャンルを変えたりする機能を予定
    url = SerectRss()
    GetRss(url)
def SerectRss():
    url = ""
    #RSSのURL
    url  = "https://news.yahoo.co.jp/pickup/economy/rss.xml"
#    rss_url  = "http://www.japantoday.com/feed/"
    url = "https://headlines.yahoo.co.jp/rss/it_nlab-c_sci.xml"
    return url
def GetRss(rss_url_):
    #RSSの取得
    feed = feedparser.parse(rss_url_)

    #RSSのタイトル
    print (feed.feed.title)
    
    news_list = []
    for entry in range(len(feed.entries)):
        #RSSの内容を一件づつ処理する
        # TODO titleでかっことその中身を消す
        title = feed.entries[entry].title
        link = feed.entries[entry].link
        try:
            category = feed.entries[entry].category
        except AttributeError:
            pass

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
        dict_ = {"title":"","text":"","link":"","category":""}
        dict_["title"] = title
        dict_["link"] = link
        try:
            dict_["category"] = category
        except:
            pass
        news_list.append(dict_)

    # 入手したデータを画面に出力
    for tmp in news_list:
        print("title:" + tmp["title"])
        print("link :" + tmp["link"])
        print("cate :" + tmp["category"])
        print("text :" + tmp["text"])
 
if __name__=="__main__":
    RssMahter()
