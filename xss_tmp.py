#coding:utf-8
#xss.txtの重複を排除
s = set()
with open("./xss.txt","r") as f:
    for i in f:
        s.add(i)
with open("./xss","w") as f:
    for i in s:
        f.write(i)
    
    
