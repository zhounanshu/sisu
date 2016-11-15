import datetime
datetime = datetime.datetime.now()
t = '2016-11-14 22:22:03'
t1 = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
print (datetime - t1).seconds // 60
