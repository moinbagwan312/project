import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1"
)

print(response.status_code)

data = response.json()

print(data)