import requests

url = "http://127.0.0.1:5000/chat"
data = {"message": "price of laptop"}

response = requests.post(url, json=data)
if response.status_code == 200:
    print(f"Bot: {response.json()['response']}")
else:
    print(f"Error: {response.status_code}, {response.text}")
