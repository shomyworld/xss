#coding:utf-8
#xssのパターンを収集して、xss.txtに入れる
import requests
from bs4 import BeautifulSoup
import pprint
from selenium import webdriver
import time
import re


def getSoup(url,s):
    r = s.get(url)
    html = r.text
    soup = BeautifulSoup(html,"html.parser")
    return soup

url = input("Input url > ")
s = requests.session()
#soup = getSoup(url,s)

driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html,"html.parser")
code = soup.find_all("code")
for i in code:
    print(i.string)

with open("./xss_pattern","a") as f:
    for i in code:
        if not isinstance(i.string,type(None)):
            f.write(i.string)
        
