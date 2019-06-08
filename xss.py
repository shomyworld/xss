# -*- coding:UTF-8 -*-
from selenium import webdriver
# from selenium.webdriver.common.alert import Alert
import time
from bs4 import BeautifulSoup
import re
import sys
import traceback
from signin import auto_login
from signin import manual_login
from signin import session_to_selenium
import argparse


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
    print("python3 xss.py")
    print("python3 xss.py -c < credential/qiita")
    print("")
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
                # JavaScriptで新規タブを開く
                driver.execute_script("window.open("+"'"+URL+"'"+", 'newtab')")
                time.sleep(1)
    else:
        print("method = post")
        for x in xss:
            data = {}
            for n in name:
                data[n] = x
                r = s.post(url, data=data)
                URL = r.url
                driver.execute_script("window.open("+"'"+URL+"'"+", 'newtab')")
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
            pattern = r"h\w+://\w+.\w+"
            res = re.match(pattern, url)
            domain = res.group()
            return domain + action
    except:
        traceback.print_exc()
        return url


def main():
    # パーサーを作る
    parser = argparse.ArgumentParser(add_help=False)

    # 引数の追加
    parser.add_argument('-f', '--firefox', action='store_true')
    parser.add_argument('-s', '--safari', action='store_true')
    parser.add_argument('-c', '--chrome', action='store_true')
    parser.add_argument('-m', '--manual', action='store_true')
    parser.add_argument('-a', '--auto', action='store_true')
    parser.add_argument('-h', '--help', action='store_true')

    # 引数を解析する
    args = parser.parse_args()

    # driverの選択
    if args.firefox:
        driver = webdriver.Firefox()
    elif args.safari:
        driver = webdriver.Safari()
    elif args.chrome:
        driver = webdriver.Chrome()
    elif args.help:
        usage()
        sys.exit(0)
    else:
        driver = webdriver.Chrome()

    # auto/manualログインの選択
    if args.manual:
        r, s, url = manual_login()
    elif args.auto:
        r, s, url = auto_login()
    else:
        r, s, url = manual_login()

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
