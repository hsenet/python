import requests
import json
response_API = requests.get("http://ifconfig.io/json/")
print(response_API)

data = response_API.text
parse_json = json.loads(data)
print("test")