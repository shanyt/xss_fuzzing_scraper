n = 5
while n > 0:
    age = int(raw_input("Plz input your age"))
    n = n - 1
    if age >= 18:
        print 'adult'
    else:
        print 'teenager'