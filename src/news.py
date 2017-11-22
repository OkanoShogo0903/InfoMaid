import requests
from bs4 import BeautifulSoup
#news_list
def GetNews():
    if 1:
        url = 'https://news.finance.yahoo.co.jp/'
    else:
        url = 'https://news.yahoo.co.jp/pickup/economy/rss.xml'

    res = requests.get(url)

    # print(res.text)
    soup = BeautifulSoup(res.text, 'lxml') #要素を抽出
    print(soup.text)

    '''
    #リンクを表示
    for a in soup.find_all('a'):
        text = a.get('href')
        print(text)         
    '''

    explains = soup.find_all("li", {"class": "ymuiArrow1"})
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

def PlayGround():    
    url = 'https://news.yahoo.co.jp/pickup/economy/rss.xml'

    res = requests.get(url)

#    print(res.text)
    soup = BeautifulSoup(res.text, 'xml') #要素を抽出
    print(soup.text)

    explains = soup.find_all("div", {"id": "webkit-xml-viewer-source-xml"})
    #explains = soup.find_all()
    news_list = []
    for explain in explains:
        # 新しく追加する辞書を構成する
        dict_ = {}
        dict_ = {"title":"","text":"","genre":"","link":""}
        dict_["title"] = explain.text.replace("\xa0","")
        dict_["text"] = ""
        news_list.append(dict_)

    # 入手したデータを画面に出力
    for tmp in news_list:
        print("title:" + tmp["title"])
        print("genre:" + tmp["genre"])
        print("link :" + tmp["link"])
        print("text :" + tmp["text"])
     
if __name__=="__main__":
    PlayGround()
#    GetNews()
