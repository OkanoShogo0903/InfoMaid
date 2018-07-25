# -*- coding: utf-8 -*-
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import time
import datetime
import re
import types

import urllib
import json

import requests
from bs4 import BeautifulSoup
# [END LibInstall]

# [START General]
# [END General]


def show_page(_email, _password):
    options = Options()
    #options.add_argument('--headless') # headlessにする方法
    #options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(width=150,height=400)

    #driver.get('http://vaaaaaanquish.hatenablog.com/entry/2017/06/06/194546')

    # Trelloのログイン画面に移動
    driver.get(trello_login_url)

    # タイムアウトで10秒待つ
    driver.implicitly_wait(10) # seconds
   
    # ID/PASSを入力
    id = driver.find_element_by_id('user')
    id.send_keys(_email)
    password = driver.find_element_by_id('password')
    password.send_keys(_password)

    # ログインボタンをクリック
    login_button = driver.find_element_by_id("login")
    login_button.click()

    time.sleep(1.5)

    # サイト内の個人活動記録画面に遷移
    driver.get(trello_individual_comment_url)
    time.sleep(1.5)

    #print(driver.page_source)
# [END LoginFunction]


def getTrelloScraping():
    surround_pattern = r'(trello_email\s*:\s*)'

    res = driver.page_source.encode('utf-8')
    my_soup = BeautifulSoup(res, 'lxml') #要素を抽出 html.parser
    main_comment_html = HandClassScraping(res.decode('utf-8')) # <div class="js-list-actions">が閉じられるまでのコードを返す

    comment_soup = BeautifulSoup(main_comment_html, 'lxml')
    # マークダウンのためにhtmlのタグとかついたテキストを持ってくる方法
    #exprains = comment_soup.find_all("div",{"class": "current-comment js-friendly-links js-open-card"})
    # ユーザがTrelloに書いたテキストをそのまま使う方法
    exprains = comment_soup.find_all("textarea",{"class": "comment-box-input js-text"})

    #print("exprains :",type(exprains)) # <class 'bs4.element.ResultSet'>
    #print(exprains) # 一つの投稿に関する投稿者や投稿時間等のデータの集まりのリスト(のようなものby BeautifulSoup公式)
    #print("******")

    modify_list = []
    for explain in exprains: # explain : <class 'bs4.element.Tag'>
        # タグを外す
        #print("contents:",type(explain.contents)) # list
        #print("contents:",type(explain.contents[0])) # tag
        #print(explain.contents[0]) # same to str(explain.contents[0])
        string = ''.join(map(str,explain.contents))
        #print(string)
        modify_list.append(string)
        
        #print("*** END ***")
    #print("*** END ***")
    return modify_list
# [END ScrapingFunction]


def main():
    show_page()

if __name__=="__main__":
    QUERY = 'hello'
    API_KEY = 'AIzaSyBehUIC3YGTC_Ms8AackUAIv2jrxxbJ-0E'
    CUSTOM_SEARCH_ENGINE_ID = '013036536707430787589:_pqjad5hr1a'
    NUM = 10

    url = 'https://www.googleapis.com/customsearch/v1?'
    params = {
	'key': API_KEY,
	'q': QUERY,
	'cx': CUSTOM_SEARCH_ENGINE_ID,
	'alt':'json',
	'lr' :'lang_en',
    }

    #for i in range(0,NUM):
    req_url = url + urllib.urlencode(params)
    res = urllib.urlopen(req_url)
    dump = json.loads(res.read())
    print(dump)
        #f.write(json.dumps(dump) + "\n")
        #if not dump['queries'].has_key('nextPage'):
        #    break
        #start = int(dump['queries']['nextPage'][0]['startIndex'])

    #main()
