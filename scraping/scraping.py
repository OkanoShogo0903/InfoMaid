import requests
from bs4 import BeautifulSoup

# 文字化け確認のため、ファイルに出力する
f = open('text.txt', 'w') # 書き込みモードで開く

url = 'https://news.finance.yahoo.co.jp/'
res = requests.get(url)

'''
html = res.text [f:id:aifinance:20170214162021p:plain]
soup = BeautifulSoup(html, "html.parser")
text_div = soup.find('div', {'class': 'ymuiContainerNopad clearFix s170'})
text_div.get_text()
text = text_div.get_text().replace('\n', '')
text = text.replace('\u3000', '')

print(text)
'''
# print(res.text)
soup = BeautifulSoup(res.text, 'lxml') #要素を抽出

for a in soup.find_all('a'):
    text = a.get('href')
    print(text)         #リンクを表示
#    f.writelines(text)

#for num in range(5):
res = []
explains = soup.find_all("li", {"class": "ymuiArrow1"})
for explain in explains:
    res.append(explain.text.replace("\xa0",""))
    res.append("\n")
f.writelines(res)

# main_body = soup.find("div", {"id": "main"})

# f.writelines(sub_body.prettify())

# main_body = soup.find("div", {"id": "main"})
# print(main_body)
# f.writelines(res.text) # シーケンスが引数。

f.close()
