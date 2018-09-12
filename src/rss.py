import feedparser
from datetime import datetime
from time import mktime
def rssMaster():
# 音声でジャンルを指定したり、ランダムなジャンルからニュースを取得したり、時間帯によって取得するジャンルを変えたりする機能を予定
    url = serectRss()
    getRssTopic(url)


def serectRss():
    ''' RSSのURLを設定 '''
    url  = "https://news.yahoo.co.jp/pickup/economy/rss.xml"
#    rss_url  = "http://www.japantoday.com/feed/"
#    url = "https://headlines.yahoo.co.jp/rss/it_nlab-c_sci.xml"
    return url


def getRssTitle(rss_url_):
    # RSSの取得
    feed = feedparser.parse(rss_url_)

    # RSSのタイトル
    return feed.feed.title


def getRssTopic(rss_url_):
    # RSSの取得
    feed = feedparser.parse(rss_url_)

    # RSSのタイトル
#    print (feed.feed.title)
    
    topic_list = []
    for entry in range(len(feed.entries)):
        # RSSの内容を一件づつ処理する
        # published_datetime等は世界時間になっているため、日本時間には+9時間すること
        # 最新の記事から順に取得される
        # TODO titleでかっことその中身を消す

        # 更新日を文字列として取得
        published_string = feed.entries[entry].published
        # 更新日をdatetimeとして取得
        tmp = feed.entries[entry].published_parsed
        published_datetime = datetime.fromtimestamp(mktime(tmp))
        # 日本時間に変換
#        jp_datetime = published_datetime + datetime.timedelta(hours=9)

        # 新しく追加する辞書を構成する
        dict_ = {"title":"","text":"","link":"","category":"","published_string":"","published_datetime":""}
        dict_["title"] = feed.entries[entry].title
        dict_["link"] = feed.entries[entry].link
        dict_["published_string"] = published_string
        dict_["published_datetime"] = published_datetime
        # categoryがない場合はエラーを吐くので、その対応
        try:
            dict_["category"] = feed.entries[entry].category
        except:
            pass
        topic_list.append(dict_)

    # 入手したデータを画面に出力
    '''
    for tmp in topic_list:
        print("title:" + tmp["title"])
        print("link :" + tmp["link"])
        print("cate :" + tmp["category"])
        print("text :" + tmp["text"])
    '''    
    return topic_list


if __name__=="__main__":
    rssMaster()
