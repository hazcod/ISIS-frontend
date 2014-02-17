import re
regex = re.compile("\040+IE: (IEEE (.+)/){0,1}WPA(\d)* Version (\d)",re.IGNORECASE|re.MULTILINE)
f = open('scanned','r')
string = ""
while 1:
    line = f.readline()
    if not line:break
    string += line

f.close()

r = regex.search(string)
print(r.groups())