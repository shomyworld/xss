# coding:utf-8
import requests
from bs4 import BeautifulSoup


def getSoup(r):
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    return soup


def login():
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
    r = s.post(url, data=element)
    print(r.text)


if __name__ == '__main__':
    login()
