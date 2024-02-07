import requests
#
# response = requests.post(
#     'http://127.0.0.1:5000/user/',
#     json={"name": "user_2", "email": "1@1.ru"},
# )
# print(response.status_code)
# print(response.text)

response = requests.get(
    'http://127.0.0.1:5000/user/',
)
print(response.status_code)
print(response.text)

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
