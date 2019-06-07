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
    r = s.post(url, data=element)
    # ログイン後のsessionをseleniumに渡す
    driver = webdriver.Chrome()
    driver.get(url)
    for name, value in s.cookies.get_dict().items():
        tmp = {}
        tmp['name'] = name
        tmp['value'] = value
        tmp['domain'] = '.qiita.com'
        driver.add_cookie(tmp)
    driver.get(url)
    driver.close()


if __name__ == '__main__':
    login()
