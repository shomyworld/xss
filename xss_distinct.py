#coding:utf-8
#xss.txtの重複を排除
s = set()
with open("./xss_duplicat","r") as f:
    for i in f:
        s.add(i)
with open("./xss_pattern","w") as f:
    for i in s:
        f.write(i)
    
    
