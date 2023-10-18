import datetime

now = datetime.datetime.now()
today8am = now.replace(hour=21, minute=0, second=0, microsecond=0)
if now < today8am:
    print('open')
else:
    print('closed')