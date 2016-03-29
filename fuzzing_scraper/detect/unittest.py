ret = 'abcdefghijklmnopq%rstuvwxyz'
for i in range(len(ret)):
    if ret[i] == '%':
        i = i + 2
    print ret[i:]