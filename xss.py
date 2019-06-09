# -*- coding:UTF-8 -*-
import time
from bs4 import BeautifulSoup
import re
from signin import session_to_selenium
from signin import arg


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


def payload():
    # xss_patternをxss配列に書き込む
    xss = []
    with open("xss_pattern", "r") as f:
        xss = f.read().splitlines()
    return xss


def xss_insert(s, url, method, xss, name, value, driver):
    if method == "get":
        print("method = get")
        for x in xss:
            data = {}
            for n, v in zip(name, value):
                if v == '' or v is None:
                    data[n] = x
                else:
                    data[n] = v  # 送信するパラメータ
            r = s.get(url, params=data)  # bug
            URL = r.url
            # JavaScriptで新規タブを開く
            driver.execute_script("window.open("+"'"+URL+"'"+", 'newtab')")
            time.sleep(3)
    else:
        print("method = post")
        for x in xss:
            data = {}
            for n, v in zip(name, value):
                if v == '' or v is None:
                    data[n] = x
                else:
                    data[n] = v  # 送信するパラメータ
            r = s.post(url, data=data)
            URL = r.url
            driver.execute_script("window.open("+"'"+URL+"'"+", 'newtab')")
            time.sleep(3)


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
            pattern = r"(?:https?|ftps?)://([A-Za-z0-9-]{1,63}\.)*(?:(com)|(org)|([A-Za-z0-9-]{1,63}\.)([A-Za-z0-9-]{1,63}))"
            res = re.match(pattern, url)
            domain = res.group()
            return domain + action
    except AttributeError:
        return url


def main():
    # xssをロードする
    xss = payload()

    # 引数を解析
    r, s, url, driver, flag = arg()

    # nologinオプションの時の処理
    if flag:
        driver.get(url)
    else:
        # ログイン後のsessionをseleniumに渡す
        session_to_selenium(r, s, url, driver)

    inputag = []
    name = []
    value = []

    # Javascriptが起動した状態のhtmlを取得
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    # formの処理
    form = soup.find("form")
    # inputag = soup.find_all("input")
    inputag = soup.form.find_all("input")
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
            xss_insert(s, action, method, xss, name, value, driver)
        elif soup.find("form").get("method").lower() == "post":
            method = "post"
            xss_insert(s, action, method, xss, name, value, driver)
        else:
            method = "get"
            xss_insert(s, action, method, xss, name, value, driver)
    # methodがないときの処理
    except AttributeError:
        method = "get"
        xss_insert(s, action, method, xss, name, value, driver)


if __name__ == '__main__':
    main()
