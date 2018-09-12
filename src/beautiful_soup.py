import requests
from bs4 import BeautifulSoup

# ほとんどがテストようのコードなので、実際に使われているのはgetNewsTextだけ.
def newsMaster():
    news_url = getNewsUrl()
    getNewsList(news_url)
    GetNewsText()


def getNewsUrl():
    url = 'https://news.finance.yahoo.co.jp/'
#    url = 'https://news.yahoo.co.jp/pickup/economy/rss.xml'
#    url = 'https://rdsig.yahoo.co.jp/rss/l/headlines/sci/it_nlab/RV=1/RU=aHR0cHM6Ly9oZWFkbGluZXMueWFob28uY28uanAvaGw_YT0yMDE3MTEyNC0wMDAwMDA3My1pdF9ubGFiLXNjaQ--'
    return url


def getNewsText(url_,pos_):
    res = requests.get(url_)
    soup = BeautifulSoup(res.text, 'lxml') #要素を抽出
    explains = soup.find_all(pos_[0], {pos_[1]: pos_[2]})

#    for explain in explains:
#        print (explain.text)  
    
    # どうせ記事は一つしかないので、配列の一番目を渡しておく
    return explains[0].text
           

def getNewsList(url_):
    res = requests.get(url_)

    # print(res.text)
    soup = BeautifulSoup(res.text, 'lxml') #要素を抽出
#    print(soup.text)

    explains = soup.find_all("li", {"class": "ymuiArrow1"})
#    explains = soup.find_all("p", {"class": "ynDetailText"})
#    explains = soup.find_all("p", {"class": "ynDetailText"})

    news_list = []
    for explain in explains:
        # 新しく追加する辞書を構成する
#        dict_ = {}
        dict_ = {"title":"","text":"","genre":"","link":""}
        dict_["title"] = explain.text.replace("\xa0","")
        dict_["text"] = ""
        news_list.append(dict_)
        #print(dict_)

    # 入手したデータを画面に出力
    for tmp in news_list:
        print("title:" + tmp["title"])
        print("genre:" + tmp["genre"])
        print("link :" + tmp["link"])
        print("text :" + tmp["text"])


if __name__=="__main__":
    newsMaster()
