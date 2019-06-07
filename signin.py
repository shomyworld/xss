# coding:utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import argparse
import sys

def usage():
    print("[*] Usage")
    print("python3 xss.py -c < credential/qiita")
    print("")
    print("cat credential/qiita")
    print("https://qiita.com/login")
    print("email")
    print("password")
    sys.exit(0)


def getSoup(r):
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    return soup


# ファイルにログイン情報を書き込んで起動時にリダイレクト入力する
def auto_login():
    url = input()
    s = requests.session()
    r = s.get(url)
    soup = getSoup(r)
    input_all = soup.form.find_all("input")
    element = {}
    for i in input_all:
        if i.get('value') is None:
            element[i.get('name')] = input()
        else:
            element[i.get('name')] = i.get('value')
    # ログイン
    r = s.post(url, data=element)
    return r, s, url


# 対話的にログインする
def manual_login():
    url = input("target url > ")
    s = requests.session()
    r = s.get(url)
    soup = getSoup(r)
    input_all = soup.form.find_all("input")
    element = {}
    for i in input_all:
        if i.get('value') is None:
            element[i.get('name')] = input(i.get('name')+' : ')
        else:
            element[i.get('name')] = i.get('value')
    # ログイン
    r = s.post(url, data=element)
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
    # パーサーを作る
    parser = argparse.ArgumentParser(add_help = False)

    # 引数の追加
    parser.add_argument('-f', '--firefox', action = "store_true")
    parser.add_argument('-s', '--safari', action = "store_true")
    parser.add_argument('-c', '--chrome', action = "store_true")
    parser.add_argument('-m', '--manual', action = "store_true")
    parser.add_argument('-a', '--auto', action = "store_true")
    parser.add_argument('-h', '--help', action = "store_true")

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

    if args.manual:
        r, s, url = manual_login()
    elif args.auto:
        r, s, url = auto_login()
    else:
        r, s, url = manual_login()

    session_to_selenium(r, s, url, driver)


if __name__ == '__main__':
    main()
