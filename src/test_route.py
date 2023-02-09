import os
import json
import requests


SERVER_URL = "http://127.0.0.1:8000"
page_url = "user/"

user = {
    "first_name": "Jim",
    "last_name": "Holden",
    "phone_number": "+38095-88-44-321",
    "age": 35
}
user2 = {
    "first_name": "Naomi",
    "last_name": "Nagata",
    "phone_number": "+38095-77-44-123",
    "age": 34
}
auth_params = ('unicorn', 'rainbow')

response = requests.post(os.path.join(SERVER_URL, page_url), data=json.dumps(user2), auth=auth_params)
print(response.status_code)
print(json.loads(response.text))

get_params = {"last_name": "Holden"}
print(requests.get(os.path.join(SERVER_URL, page_url), params=get_params, auth=auth_params).text)
none_params = {"last_name": "Snow"}
print(requests.get(os.path.join(SERVER_URL, page_url), params=none_params, auth=auth_params).text)
print(requests.get(os.path.join(SERVER_URL, page_url), params=none_params).text)
