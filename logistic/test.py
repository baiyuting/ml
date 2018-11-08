import urllib
from http.client import HTTPConnection
from urllib.parse import urlencode

test_data = {'content': '这个我的QQ213456876'}
test_data_urlencode = urlencode(test_data)

access_token = '24.a70c44fc26063a60438d365555d4c51b.2592000.1544166505.282335-11521443'
requrl = "https://aip.baidubce.com/rest/2.0/antispam/v1/spam?access_token="+access_token
headerdata = {"Content-Type": "application/x-www-form-urlencoded"}

conn = HTTPConnection("aip.baidubce.com")

conn.request(method="POST", url=requrl, body=test_data_urlencode, headers=headerdata)

response = conn.getresponse()

res = response.read()

print(res)
