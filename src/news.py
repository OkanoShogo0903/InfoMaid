import requests
from bs4 import BeautifulSoup
def GetNews():
    url = 'https://news.finance.yahoo.co.jp/'
    res = requests.get(url)

    # print(res.text)
    soup = BeautifulSoup(res.text, 'lxml') #要素を抽出

    '''
    #リンクを表示
    for a in soup.find_all('a'):
        text = a.get('href')
        print(text)         
    '''
    res = []
    explains = soup.find_all("li", {"class": "ymuiArrow1"})
    for explain in explains:
        res.append(explain.text.replace("\xa0",""))
        res.append("\n")
    print(res)
    
    # main_body = soup.find("div", {"id": "main"})
    
    # f.writelines(sub_body.prettify())
    
    # main_body = soup.find("div", {"id": "main"})
    # print(main_body)
    # f.writelines(res.text) # シーケンスが引数。
    
if __name__=="__main__":
    GetNews()
