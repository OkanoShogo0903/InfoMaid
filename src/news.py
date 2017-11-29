import time
import threading
import beautiful_soup
import rss
news_list = []
site_list = [\
    {
        'RSS_URL':
            'https://headlines.yahoo.co.jp/rss/it_nlab-c_sci.xml',
        'TEXT_POS':[
            'p','class','ynDetailText'
        ],
    },
]
class NewsData:
    """News infomation class"""
    def __init__(self,site_):
        # RSSのURLと記事があるサイト
        self.RSS_URL = site_['RSS_URL']
        # 記事の位置（手動で探してsite_listに書いたやつ）
        self.TEXT_POS = site_['TEXT_POS']

        self.SITE_NAME = ""
        
        # RSS自体のタイトルを取得
        self.RSS_TITLE = rss.get_rss_title(self.RSS_URL)

        # RSSから各記事のタイトルとURLを取得
        self.topic_list = rss.get_rss_topic(self.RSS_URL)
        
        # 記事があるURLを手に入れる
        for topic in self.topic_list:
            topic["text"] = beautiful_soup.get_news_text( topic["link"], self.TEXT_POS)

    def print_all_topic(self):
        print("---------------------------------------------------")
        for topic in self.topic_list:
            print("title:" + topic["title"])
            print("link :" + topic["link"])
            print("cate :" + topic["category"])
            a = topic["text"]
            print("text :" + a[:50])
#            print("text :" + topic["text"])
        print("---------------------------------------------------")

    def __str__(self):
        res =       " RSS_URL  : " + self.RSS_URL + "\r\n"
        res = res + " TEXT_POS : " + (str)(self.TEXT_POS)
        return res

def news_init():
    global news_list
# threads start
    data_renew()

    for news in news_list:
        news.print_all_topic()
    print(len(news_list))
    
#    t=threading.Timer(1,data_renew)
def data_renew():
    global news_list
    renew_data_list = []
    for site in site_list:
        tmp = NewsData(site)
#        tmp.print_all_topic()
#        print (tmp)
        renew_data_list.append(tmp)

    news_list = renew_data_list

# 一時間ごとにデータを更新するために１時間後に呼び出す
#    t=threading.Timer(60*60,data_renew)

if __name__=="__main__":
    news_init()
