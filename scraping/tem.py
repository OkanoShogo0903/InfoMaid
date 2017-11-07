'''
import requests
from bs4 import BeautifulSoup
from flask import jsonify
def make_soup_from(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)
    return soup

def translate_from_yahoo(word):
    url = "http://kotobank.jp/ejword/{}?dic=pej4&oid=SPEJ00339000".format(word)
    soup = make_soup_from(url)
    res = []
    explains = soup.find_all("div",{"class":"explain"})
    for explain in explains:
        res.append(explain.text.replace("\n",""))
    return "\n".join(res)

if __name__ == "__main__":
    word = input("type your word?\n ")
    print("result is ")
    print(translate_from_yahoo(word))
'''

# import urllib2
import requests
from bs4 import BeautifulSoup

url = "http://news.yahoo.co.jp/"
res = requests.get(url)

# get first all html source
soup = BeautifulSoup(res, "html.parser")

# extract main body which tag is div
main_body = soup.find("div", {"id": "main"})

# extract list items in main_body which class name equals to "topics"
topics = main_body.find("ul", {"class": "topics"})

# join each list item's string
out_str = ""
for first_topic in topics.find("li").a.contents:
    out_str += first_topic.string

# remove if string contains "new"
out_str = re.sub(r'new', '', out_str)

# output
print (out_str)
