# -*- coding:UTF-8 -*-
import time
from bs4 import BeautifulSoup
import re
from signin import session_to_selenium
from signin import arg
from selenium.webdriver.common.alert import Alert
from selenium.common import exceptions


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
    with open("xss_tmp_pattern", "r") as f:
        xss = f.read().splitlines()
    return xss


def xss_insert_requests(s, url, method, xss, name, value, driver):
    if method == "get":
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
    else:
        print(url)
        for x in xss:
            data = {}
            for n, v in zip(name, value):
                if v == '' or v is None:
                    data[n] = x
                else:
                    data[n] = v  # 送信するパラメータ
            print(data)
            proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
            r = s.post(url, data=data, proxies=proxies, verify=False)
            URL = r.url
            driver.execute_script("window.open("+"'"+URL+"'"+", 'newtab')")


def xss_insert_selenium(xss, name, value, type_, driver):
    for x in xss:
        for n, v, t in zip(name, value, type_):
            if v == '' or v is None:
                driver.find_element_by_name(n).send_keys(x)
            elif t == "submit":
                submit = driver.find_element_by_name(n)
        submit.click()
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
            pattern = r"(?:https?|ftps?)://([A-Za-z0-9-]{1,63}\.)*(?:(com)|(org)|([A-Za-z0-9-]{1,63}\.)([A-Za-z0-9-]{1,63})):?[0-9]*"
            res = re.match(pattern, url)
            domain = res.group()
            return domain + action
    except AttributeError:
        return url


def create_report():
    with open("report","w") as f:
        f.write("aaaa")


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

    # Javascriptが起動した状態のhtmlを取得
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    # 自動遷移
    pattern = r"(?:https?|ftps?)://([A-Za-z0-9-]{1,63}\.)*(?:(com)|(org)|([A-Za-z0-9-]{1,63}\.)([A-Za-z0-9-]{1,63})):?[0-9]*"
    res = re.match(pattern, url)
    base_url = res.group()
    a = soup.find_all("a")
    URL = []
    for i in a:
        if i.get("href") is not None and str(i.get("href"))[0] == '/':
            URL.append(base_url + i.get("href"))
    c = 0
    for u in URL:
        """
        if u == 'http://13.230.216.189:3000/users/4/paid_time_off' or u == 'http://13.230.216.189:3000/users/4/account_settings':
            continue
        """
        c += 1
        print("-------------------------------------------ページ{}----------------------------------------------------".format(c))
        print("[+] 現在URL :", u)
        if 'logout' not in str(u):
            driver.get(u)
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "html.parser")
            # formの処理
            for form in soup.find_all("form"):
                flag = False
                if form is not None:
                    for i in form.find_all("input"):
                        if i.get("type") == "text" or i.get("type") == "radio" or i.get("type") == "textarea" or i.get("type") == "checkbox":
                            flag = True
                    if not flag:
                        continue
                    inputag = form.find_all("input")
                    name = []
                    value = []
                    type_ = []

                    for i in range(len(inputag)):
                        name.append(inputag[i].get("name"))
                        value.append(inputag[i].get("value"))
                        type_.append(inputag[i].get("type"))
                    try:
                        xss_insert_selenium(xss, name, value, type_, driver)
                    except exceptions.UnexpectedAlertPresentException:
                        print("UnexpectedAlertPresentException")
                        Alert(driver).accept()
                        # driver.close()
                    except exceptions.WebDriverException:
                        print("pass")
                    """
                    except WebDriverException:
                        print("WebDriverException")
                        Alert(driver).accept()
                    """
                    """

                    if isinstance(form.get("action"), type(None)) or form.get("action") == "#":
                        action = u
                    else:
                        action = base_url + form.get("action")
                        # action = check_url(soup, u)
                    # xss入力
                    try:
                        if form.get("method").lower() == "get":
                            method = "get"
                            xss_insert_requests(s, action, method, xss, name, value, driver)
                        elif form.get("method").lower() == "post":
                            method = "post"
                            xss_insert_requests(s, action, method, xss, name, value, driver)
                        else:
                            method = "get"
                            xss_insert_requests(s, action, method, xss, name, value, driver)
                    # methodがないときの処理
                    except AttributeError:
                        method = "get"
                        xss_insert_requests(s, action, method, xss, name, value, driver)
                    """
    create_report()


if __name__ == '__main__':
    main()
