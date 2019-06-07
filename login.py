# coding:utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def getSoup(r):
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    return soup


def login():
    # url = input("target url > ")
    url = input()
    s = requests.session()
    r = s.get(url)
    soup = getSoup(r)
    input_all = soup.form.find_all("input")
    element = {}
    for i in input_all:
        if i.get('value') is None:
            # element[i.get('name')] = input(i.get('name')+' : ')
            element[i.get('name')] = input()
        else:
            element[i.get('name')] = i.get('value')
    # ログイン
    r = s.post(url, data=element)
    return r, s, url


# ログイン後のsessionをseleniumに渡す
def session_to_selenium(r, s, url):
    driver = webdriver.Chrome()
    # ページをGETして、クッキーを取得
    driver.get(url)
    domain = driver.get_cookies()[0]['domain']
    # クッキー削除
    driver.delete_all_cookies()
    # ログイン後のクッキーを追加
    for name, value in s.cookies.get_dict().items():
        tmp = {}
        tmp['name'] = name
        tmp['value'] = value
        tmp['domain'] = domain
        driver.add_cookie(tmp)
    # ログイン後のページを表示
    driver.get(url)


if __name__ == '__main__':
    r, s, url = login()
    session_to_selenium(r, s, url)
