import time
from datetime import datetime 
import threading
import jtalk
import beautiful_soup
import rss
import site_list
news_list = []
class NewsData:
    """News infomation class"""
    def __init__(self,site_):
        # RSSのURLと記事があるサイト
        self.RSS_URL = site_['RSS_URL']
        # 記事の位置（手動で探してsite_listに書いたやつ）
        self.TEXT_POS = site_['TEXT_POS']
        # サイトの名前を取得
        self.SITE_NAME = site_['SITE_NAME']
        
        # RSS自体のタイトルを取得
        self.RSS_TITLE = rss.get_rss_title(self.RSS_URL)

        # RSSから各記事の情報を取得
        self.topic_list = rss.get_rss_topic(self.RSS_URL)
        
        # 記事があるURLに接続して記事を取得する
        for topic in self.topic_list[:3]:
            topic["text"] = beautiful_soup.get_news_text( topic["link"], self.TEXT_POS)

    def say_topic(self,lim_):
        jtalk.jtalk(self.SITE_NAME)
        for topic in self.topic_list[:lim_]:
            jtalk.jtalk(topic["title"])
#            jtalk.jtalk(topic["text"])
        # 指定秒間スリープする
        time.sleep(1)

    def renew(self):
    # 新しいニュースを配列の先頭にいれる
        # RSSから各記事の情報を取得
        check_list = rss.get_rss_topic(self.RSS_URL)
        insert_list = []
        # 新しく追加される分のtopicをinsert_listにまとめる
        for topic in check_list:
            if self.topic_list[0]["published_datetime"] < topic["published_datetime"]:
                # 新しいデータを発見
                print("新しいデータを見つけた")
                # 新しいものから昇順になるようにいれる
                insert_list.append(topic)
                print(topic["title"])
                continue
            else:
                print("古いデータを見つけたのでbreak")
                break
        
        # 新しいデータをいれて古いデータを消すよ
        # insert_listが空の時はなにもしない
        if len(insert_list) != 0:
            # insert_listを既存のニュースリストの先頭にいれる
            self.topic_list = insert_list + self.topic_list
            # 追加したトピックの数だけ、古いニュースを消す
            for del_num in insert_list:
                self.topic_list.pop()
            '''
            for topic in insert_list:
                self.topic_list.insert(0,topic)
            '''
    def print_topic(self,lim_):
        count = 0
        print("---------------------------------------------------")
        print(self.SITE_NAME)
        for topic in self.topic_list[:lim_]:
            print("num  : " + str(count))
            print("title: " + topic["title"])
            #print("link :" + topic["link"])
            print("time : " + topic["published_string"])
#            print(topic["published_datetime"].day)
#            print(topic["published_datetime"].hour)
            print("cate : " + topic["category"])
            print("text : " + topic["text"][:50])
            print()
            count += 1
        print("---------------------------------------------------")

#------------------------------------------------------------------------
# 外部からは見えない部分
def data_renew():
# renewで古いニュースを破棄して、新しいデータを取得する
    print("data_renew : start")

    global news_list
    for news in news_list:
        news.renew()

    # 一時間ごとにデータを更新するために１時間後に呼び出す
    t=threading.Timer(60*60,data_renew)
    t.start()

    print("data_renew : end")
    print()

#-----------------------------------------------------------------------
# 外から呼び出される部分
def news_init():
    global news_list

    renew_data_list = []
    for site in site_list.site_list:
        tmp = NewsData(site)
        renew_data_list.append(tmp)

    news_list = renew_data_list

    # 一時間ごとにデータを更新するために１時間後に呼び出す
    t=threading.Timer(60*60,data_renew)
    t.start()

def say_news(site_name,lim_):
    global news_list
    try:
        for n in news_init:
            if n[SITE_NAME] == site_name:
                n.print_topic(lim_)
    except:
        pass
    
#-----------------------------------------------------------------------
if __name__=="__main__":
    # initでニュースを取得してくる
    news_init()
    for news in news_list:
        news.print_topic(5)
        news.say_topic(3)
