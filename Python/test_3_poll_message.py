import requests

client_id = "testclient"
url = f"http://localhost:8001/api/poll/{client_id}"

response = requests.get(url)
data = response.json()

print("Polling result:", data)
