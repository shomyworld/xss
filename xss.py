#-*- coding:UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time
from bs4 import BeautifulSoup 
import requests 
import re 
import sys
import traceback
import pprint

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


def login(url,s,name,value):
    data = {}
    for i in range(len(name)):
        if isinstance(value[i],type(None)):
            print(name[i],end=" : ")
            data[name[i]] = input("")
        else:
            data[name[i]] = value[i]
    r = s.post(url,data=data)
    return r


def xss_insert(s,url,method,xss,name):
    if method == "get":
        print("method = get")
        for x in xss:
            data = {}
            for n in name:
                data[n] = x   #送信するパラメータ
                r = s.get(url,params=data)
                URL = r.url
                driver.execute_script("window.open("+"'"+URL+"'" +", 'newtab')") #JavaScriptで新規タブを開く
                time.sleep(1)
    else:
        print("method = post")
        for x in xss:
            data = {}
            for n in name:
                data[n] = x  
                r = s.post(url,data=data)
                URL = r.url
                driver.execute_script("window.open("+"'"+URL+"'" +", 'newtab')")
                time.sleep(1)


#相対URLか絶対URLかで、送信先を決める
def check_url(soup,url):
    try:
        action = soup.find("form").get("action")
        #actionがhttpから始まる場合の処理
        if not isinstance(re.match("http",action),type(None)):
            return action
        #actionがhttpから始まらない場合の処理
        #domain+action
        else:
            pattern="h\w+://\w+.\w+"
            res = re.match(pattern,url)
            domain = res.group()
            return domain + action
    except:
        traceback.print_exc()
        return url

#xss_patternから、xssのパターンをxss配列に書き込む
xss = []
with open("xss_pattern","r") as f:
    xss = f.read().splitlines()

url = input("Target URL : ")
#オプションによって、開くブラウザを変更する
try:
    if sys.argv[1] == "-f":
        driver = webdriver.Firefox()
    elif sys.argv[1] == "-s":
        driver = webdriver.Safari()
except:
    driver = webdriver.Chrome()

s = requests.session()
inputag = []
name = []
value = []

driver.get(url)
#Javascriptが起動した状態のhtmlを取得
html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html,"html.parser")

#formの処理
form = soup.find("form")
inputag = soup.find_all("input")
for i in range(len(inputag)-1):
    name.append(inputag[i].get("name"))
    value.append(inputag[i].get("value"))
print("name = ",name) 
print("value = ",value)

if isinstance(form.get("action"),type(None)):
    action = url
else:
    action = check_url(soup,url)

print("action = ",action)

#ログインに渡すURLはformのaction属性で、指定されていない場合は、元のurlを指定する
r = login(action,s,name,value)
print(r.text)
"""
#xss入力
try:
    if soup.find("form").get("method").lower() == "get":
        method = "get"
        xss_insert(s,action,method,xss,name)
    elif soup.find("form").get("method").lower() == "post":
        method = "post"
        xss_insert(s,action,method,xss,name)
    else:
        method = "get"
        xss_insert(s,action,method,xss,name)
#methodがないときの処理
except:
   method = "get" 
   xss_insert(s,action,method,xss,name)
"""
