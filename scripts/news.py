import time
from datetime import datetime 
import threading
import random

import jtalk
import beautiful_soup
import rss
import site_list
import common_function as common
import event_master as event

# site_listで定義されたサイトごとにNewsDataを持つ.
# NewsDataはコンストラクタでニュースのロードを行うが、その際に時間がかかる.
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
        self.RSS_TITLE = rss.getRssTitle(self.RSS_URL)

        # RSSから各記事の情報を取得
        self.topic_list = rss.getRssTopic(self.RSS_URL)
        
        # 記事があるURLに接続して記事を取得する
        for topic in self.topic_list[:3]:
            topic["text"] = beautiful_soup.getNewsText( topic["link"], self.TEXT_POS)


    def sayTopic(self,say_news_num):
        jtalk.jtalk(self.SITE_NAME + "のニュースをお伝えします")
        for topic in self.topic_list[:say_news_num]:
            jtalk.jtalk(topic["title"])
            jtalk.jtalk(topic["text"])
            time.sleep(2) # 次のニュースまで一定の間隔をあける


    def renew(self):
    # 新しいニュースを配列の先頭にいれる
        # RSSから各記事の情報を取得
        check_list = rss.getRssTopic(self.RSS_URL)
        insert_list = []
        # 新しく追加される分のtopicをinsert_listにまとめる
        for topic in check_list:
            if self.topic_list[0]["published_datetime"] < topic["published_datetime"]:
                # 新しいデータを発見
                # 新しいものから昇順になるようにいれる
                insert_list.append(topic)
                print(topic["title"])
                continue
            else:
                # 古いデータにたどり着いたので、このサイトでのデータ更新終了
                break
        
        # 新しいデータをいれて古いデータを消すよ
        # insert_listが空の時はなにもしない
        if len(insert_list) != 0:
            # insert_listを既存のニュースリストの先頭にいれる
            self.topic_list = insert_list + self.topic_list
            # 追加したトピックの数だけ、古いニュースを消す
            for topic in insert_list:
                self.topic_list.pop()


#------------------------------------------------------------------------
class News:
    def __init__(self):
        # ここで生成するnews_listを使い倒していくよ
        self.news_list = self.getNewsList()              

        # 一時間ごとにデータを更新するために１時間後に呼び出す
        self.INTERVAL_SEC = 60*60 # 1時間 ごとに更新
        threading.Timer(self.INTERVAL_SEC,self.renewNewsList).start()

        # 外部から呼び出される時のためのスレッドの作成
        threading.Thread(\
                target=self.waitEventCall,\
                name="NewsEvent",\
                daemon=True\
                ).start()


    def waitEventCall(self):
        while 1:
            event.news_event.wait()
            event.news_event.clear()
            self.sayNews(say_news_num=3, is_random=True)


    def getNewsList(self):
        renew_data_list = []

        for i,site in enumerate(site_list.site_list):
            # 進行度の表示
            n = NewsData(site)
            renew_data_list.append(n)
            print("NEWS SITE PROCEEDINGS ... " + str( 100*((i+1)/len(site_list.site_list))) + "%")
        print("COMPLEAT!!")
        return renew_data_list


    # renewで古いニュースを破棄して、新しいデータを取得する
    def renewNewsList(self):
        print("news_data_renew : start")

        for news in self.news_list:
            news.renew()

        t=threading.Timer(self.INTERVAL_SEC,self.renewNewsList)
        t.start()

        print("news_data_renew : end\n")


    def sayNews(self, site_name=None, say_news_num=3, is_random=True):
        # If is_random is true, site_name will be not use.
        # If do not set site_name and is_random=False, program will occure errer.
        if is_random == True:
            site_name = random.choice(site_list.site_list)['SITE_NAME']

        try:
            for n in self.news_list:
                if n.SITE_NAME == site_name:
                    n.sayTopic(say_news_num)
        except:
            print("ニュース名でエラー")
        

news_class = News()
#-----------------------------------------------------------------------
if __name__=="__main__":
    # initでニュースを取得してくる
    #news_class = News()
    news_class.sayNews("ねとらぼ",3, is_random=True)
    print("END")
