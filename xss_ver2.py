#指定したURLにxss.txtにあるXSSパターンをすべて打ち込むスクリプト
#inputタグがあるフォームにしか使えない
#なぜかPOSTもできない
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time
from bs4 import BeautifulSoup
import requests

#xss.txtから、xssのパターンをxss配列に書き込む
xss = []
with open("xss.txt","r") as f:
    xss = f.read().splitlines()

driver = webdriver.Chrome()
#url="http://bogus.jp/xsssample/xsssample_01.php"
#url = "http://bogus.jp/xsssample/xsssample_02_M9eec.php"
#url = "http://bogus.jp/xsssample/xsssample_03_J4Skr.php"
#url = "http://bogus.jp/xsssample/xsssample_04_C_HD-.php"
url = "http://bogus.jp/xsssample/xsssample_05_3S7LA.php" #できない
#url="http://bogus.jp/xsssample/xsssample_06_w6k2v.php"
#url="http://bogus.jp/xsssample/xsssample_07_qqoXM.php"
#url="http://bogus.jp/xsssample/xsssample_08_sv8ec.php"
#url="http://bogus.jp/xsssample/xsssample_11.php" #できない
#ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
r1 = requests.get(url)
html1 = r1.text
soup1 = BeautifulSoup(html1,"html.parser")
input = []
name = []
input = soup1.find_all("input")
for i in range(len(input)-1):
     name.append(input[i].get("name"))
driver.get(url)

#xss入力
if soup1.find("form").get("method") == "GET" or soup1.find("form").get("method") == "get":
    for x in xss:
        data = {}
        for n in name:
            data[n] = x   #送信するパラメータ
            r2 = requests.get(url,params=data)
            URL = r2.url
            driver.execute_script("window.open("+"'"+URL+"'" +", 'newtab')") #JavaScriptで新規タブを開く

elif soup1.find("form").get("method") == "POST" or soup1.find("form").get("method") == "post":
    for x in xss:
        data = {}
        for n in name:
            data[n] = x
            r2 = requests.post(url,data=data)
            URL = r2.url
            driver.execute_script("window.open("+"'"+URL+"'"  +", 'newtab')")
