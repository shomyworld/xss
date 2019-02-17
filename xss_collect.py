#coding:utf-8
#xssのパターンを収集して、xssに入れる
import requests
from bs4 import BeautifulSoup
import pprint

def getSoup(url,s):
    r = s.get(url)
    html = r.text
    soup = BeautifulSoup(html,"html.parser")
    return soup

url = "https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet"
#url = "https://jpcertcc.github.io/OWASPdocuments/CheatSheets/XSSFilterEvasion.html"
s = requests.session()
soup = getSoup(url,s)
pre = soup.find_all("pre")
for i in pre:
    print(i.string)
with open("./xss_duplicat","a") as f:
    for i in pre:
        if not isinstance(i.string,type(None)):
            f.write(i.string)
        
