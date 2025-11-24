import urllib
import urllib2
import json

url = 'https://sbpaymentservices.payfort.com/FortAPI/paymentApi';
arrData = {
'command':'CAPTURE',
'access_code':'zx0IPmPy5jp1vAz8Kpg7',
'merchant_identifier':'CycHZxVj',
'merchant_reference':'XYZ9239-yu898',
'amount':'10000',
'currency':'AED',
'language':'en',
'fort_id':'149295435400084008',
'signature':'7cad05f0212ed933c9a5d5dffa31661acf2c827a',
'order_description':'iPhone 6-S',
}

values = json.dumps(arrData)
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
page = response.read()
print (page + '\n\n')