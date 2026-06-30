import requests

payload = {
    "title": "Learning APIs",
    "body": "Day 2 Practice",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=payload
)

print(response.status_code)
print(response.json())