import hashlib
import time

# print(time.time())
#
# data = '23123'
# number = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
# print(number)

appid = '5c1234b7'
curtime = int(time.time())
param = 'ew0KICAgICJ0eXBlIjogImRlcGVuZGVudCINCn0='
apikey = 'f39a239a8d5ab76fe7da9cd655599a0f'
check_sum = hashlib.md5((apikey + str(curtime)  + param).encode(encoding='UTF-8')).hexdigest()
print(curtime)
print(check_sum)
