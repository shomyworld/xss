# -*- coding:UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time
from bs4 import BeautifulSoup
# import requests
import re
import sys
import traceback
# import pprint
import getopt
from signin import *


class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

logo = '''
   _  ____________    ______            __
  | |/ / ___/ ___/   /_  __/___  ____  / /
  |   /\__ \\__ \     / / / __ \/ __ \/ /
 /   |___/ /__/ /    / / / /_/ / /_/ / /
/_/|_/____/____/    /_/  \____/\____/_/
                                          '''

print(pycolor.RED+logo+pycolor.END+"\n")


def usage():
    print("[*] Usage")
    print("python3 xss.py -c < credential/qiita")
    print("cat credential/qiita")
    print("https://qiita.com/login")
    print("email")
    print("password")
    sys.exit(0)


def payload():
    # xss_patternをxss配列に書き込む
    xss = []
    with open("xss_pattern", "r") as f:
        xss = f.read().splitlines()
    return xss


def xss_insert(s, url, method, xss, name, driver):
    if method == "get":
        print("method = get")
        for x in xss:
            data = {}
            for n in name:
                data[n] = x  # 送信するパラメータ
                r = s.get(url, params=data)
                URL = r.url
                driver.execute_script("window.open("+"'"+URL+"'" +", 'newtab')") # JavaScriptで新規タブを開く
                time.sleep(1)
    else:
        print("method = post")
        for x in xss:
            data = {}
            for n in name:
                data[n] = x
                r = s.post(url, data=data)
                URL = r.url
                driver.execute_script("window.open("+"'"+URL+"'" +", 'newtab')")
                time.sleep(1)


# 相対URLか絶対URLかで、送信先を決める
def check_url(soup, url):
    try:
        action = soup.find("form").get("action")
        # actionが(http||https)から始まる場合の処理
        # if not isinstance(re.match("http",action),type(None)):
        if "http" in action:
            return action
        # actionがhttpから始まらない場合の処理
        else:
            pattern="h\w+://\w+.\w+"
            res = re.match(pattern, url)
            domain = res.group()
            return domain + action
    except:
        traceback.print_exc()
        return url


def main():

    if not len(sys.argv[1:]):
        usage()

    # ログイン処理
    r, s, url = login()

    # コマンドラインオプションの読み込み
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cfs:")
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-f", "--firefox"):
            driver = webdriver.Firefox()
        elif o in ("-s", "--safari"):
            driver = webdriver.Safari()
        elif o in ("-c", "--chrome"):
            driver = webdriver.Chrome()
        else:
            usage()

    # ログイン後のsessionをseleniumに渡す
    session_to_selenium(r, s, url, driver)

    # xssをロードする
    xss = payload()

    inputag = []
    name = []
    value = []

    # Javascriptが起動した状態のhtmlを取得
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    # formの処理
    form = soup.find("form")
    inputag = soup.find_all("input")
    for i in range(len(inputag)-1):
        name.append(inputag[i].get("name"))
        value.append(inputag[i].get("value"))
    print("name = ", name)
    print("value = ", value)
    print("form =", form)

    if isinstance(form.get("action"), type(None)):
        action = url
    else:
        action = check_url(soup, url)

    print("action = ", action)

    # xss入力
    try:
        if soup.find("form").get("method").lower() == "get":
            method = "get"
            xss_insert(s, action, method, xss, name, driver)
        elif soup.find("form").get("method").lower() == "post":
            method = "post"
            xss_insert(s, action, method, xss, name, driver)
        else:
            method = "get"
            xss_insert(s, action, method, xss, name, driver)
    # methodがないときの処理
    except:
       method = "get"
       xss_insert(s, action, method, xss, name, driver)


if __name__ == '__main__':
    main()
