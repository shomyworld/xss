# coding:utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import argparse
import sys
import re


def usage():
    print("[*] Usage")
    print("python3 xss.py -c < credential/qiita")
    print("")
    print("cat credential/qiita")
    print("https://qiita.com/login")
    print("email")
    print("password")
    sys.exit(0)


def arg():
    # パーサーを作る
    parser = argparse.ArgumentParser(add_help=False)

    # 引数の追加
    parser.add_argument('-f', '--firefox', action='store_true')
    parser.add_argument('-s', '--safari', action='store_true')
    parser.add_argument('-c', '--chrome', action='store_true')
    parser.add_argument('-m', '--manual', action='store_true')
    parser.add_argument('-a', '--auto', action='store_true')
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('-n', '--nologin', action='store_true')

    # 引数を解析する
    args = parser.parse_args()
    if args.firefox:
        driver = webdriver.Firefox()
    elif args.safari:
        driver = webdriver.Safari()
    elif args.chrome:
        driver = webdriver.Chrome()
    elif args.help:
        usage()
        sys.exit()
    else:
        driver = webdriver.Chrome()

    if args.nologin:
        r, s, url = nologin()
        return r, s, url, driver, True
    elif args.manual:
        r, s, url = manual_login(driver)
        return r, s, url, driver, False
    elif args.auto:
        r, s, url = auto_login(driver)
        return r, s, url, driver, False
    else:
        r, s, url = manual_login(driver)
        return r, s, url, driver, False


def getSoup(r):
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    return soup


# 相対URLか絶対URLかで、送信先を決める
def check_url(soup, url):
    try:
        action = soup.get("action")
        # 絶対URLの場合
        if "http" in action:
            return action
        # 相対URLの場合
        else:
            if str(action)[0] != '/':
                action = '/'+action
            pattern = r"(?:https?|ftps?)://([A-Za-z0-9-]{1,63}\.)*(?:(com)|(org)|([A-Za-z0-9-]{1,63}\.)([A-Za-z0-9-]{1,63})):?[0-9]*"
            res = re.match(pattern, url)
            domain = res.group()
            return domain + action
    except AttributeError:
        return url


# ファイルにログイン情報を書き込んで起動時にリダイレクト入力する
def auto_login(driver):
    url = input()
    s = requests.session()
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    for cookie in driver.get_cookies():
        s.cookies.set(cookie["name"], cookie["value"])
    form = []
    for i in soup.find_all("form"):
        for j in i.find_all("input"):
            if j.get("type").lower() == "password":
                form.append(i)
                break
    input_all = form[0].find_all("input")
    url = check_url(form[0], url)
    element = {}
    for i in input_all:
        if i.get('value') is None or i.get('value') == '':
            element[i.get('name')] = input(i.get('name')+' : ')
        else:
            element[i.get('name')] = i.get('value')
    # ログイン
    print(url)
    r = s.post(url, data=element)
    print(r.status_code)
    return r, s, url


# 対話的にログインする
def manual_login(driver):
    url = input("target url > ")
    s = requests.session()
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    for cookie in driver.get_cookies():
        s.cookies.set(cookie["name"], cookie["value"])
    form = []
    for i in soup.find_all("form"):
        for j in i.find_all("input"):
            if j.get("type").lower() == "password":
                form.append(i)
                break
    input_all = form[0].find_all("input")
    url = check_url(form[0], url)
    element = {}
    for i in input_all:
        if i.get('value') is None or i.get('value') == '':
            element[i.get('name')] = input(i.get('name')+' : ')
        else:
            element[i.get('name')] = i.get('value')
    # ログイン
    print(url)
    r = s.post(url, data=element)
    print(r.status_code)
    return r, s, url


# ログイン機能のいらないサイト
def nologin():
    url = input("target url > ")
    s = requests.session()
    r = s.get(url)
    return r, s, url


# ログイン後のsessionをseleniumに渡す
def session_to_selenium(r, s, url, driver):
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


def main():
    r, s, url, driver, boolean = arg()
    session_to_selenium(r, s, url, driver)


if __name__ == '__main__':
    main()
