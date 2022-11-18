import requests

url = "https://filereceiver.cwb.gov.tw/api/file"

payload = {'username': 'account',
'apikey': 'apitoken',
'vdir': '/test'}
files = [
  ('upload_file', open('/test.txt','rb'))
]
headers = {
 'Content-Type': 'multipart/form-data' 
}

response = requests.request("POST", url,  data = payload, files = files)

print(response.text.encode('utf8'))

