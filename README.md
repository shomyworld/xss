XSS TOOL
===
Overview

## Description
- input xss_patern form of url specified
- auto login function
- manual login function

## Ticket
- There are seveal form,input xss_patern each form
- add detect xss auditor function
- add auto page transition function

## Requirement
- python3
- pip3 install -r requirements.txt

## Usage
usage: python3 xss.py ([-h]|[-f]|[-s]|[-c])[-m]
usage: python3 xss.py ([-h]|[-f]|[-s]|[-c])[-a] < credential/qiita

optional arguments:
  -h, --help     show this help message and exit
  -f, --firefox  with Firefox
  -s, --safari   with Safari
  -c, --chrome   with Chrome
  -m, --manual   manual login
  -a, --auto     auto login

cat credential/qiita

https://qiita.com/login
email
password
