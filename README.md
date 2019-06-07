# XSS自動化
- 指定したURLのフォームに、xss_patternを打ち込む
- 自動ログイン機能
- 手動ログイン機能

## チケット
- formが複数ある場合、それぞれのformにxss_patternを打ち込めるようにする
- xss auditorの検知機能の追加
- 自動ページ遷移機能の追加

## 使い方
python3 xss.py -c < credential/qiita

cat credential/qiita

https://qiita.com/login
email
password
