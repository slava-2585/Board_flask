import requests
#
response = requests.post(
    'http://127.0.0.1:5000/adv/',
    json={"title": "Стиралка", "description": "Стриральная машина с сушкой"},
    headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNzczODIwOSwianRpIjoiYWY0MTYyNDYtYjk5Yy00OTYxLTlkOWEtZmVjNzdhMjU1M2ZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNzA3NzM4MjA5LCJjc3JmIjoiNTFjNWJiYWEtMzAyYy00ODZmLTg5NDgtMGE0N2ZiZTRlMjFhIiwiZXhwIjoxNzA5ODExODA5fQ.FtwzWfj6svgfgCz1jcXv5ZMmwmBs7M4duc5pozf8_wc"}
)
print(response.status_code)
print(response.text)

# response = requests.get(
#     'http://127.0.0.1:5000/user/',
# )
# print(response.status_code)
# print(response.text)

# response = requests.get(
#     'http://127.0.0.1:5000/user/600/',
# )
# print(response.status_code)
# print(response.text)

# response = requests.patch(
#     'http://127.0.0.1:5000/user/4/',
#     json={"name": "new_user_2", "password": "R"}
# )
# print(response.status_code)
# print(response.text)
#
# response = requests.get(
#     'http://127.0.0.1:5000/user/1/',
# )
# print(response.status_code)
# print(response.text)


# response = requests.delete(
#     "http://127.0.0.1:5000/user/4/",
# )
# print(response.status_code)
# print(response.text)
#
# response = requests.get(
#     "http://127.0.0.1:5000/user/4/",
# )
# print(response.status_code)
# print(response.text)
