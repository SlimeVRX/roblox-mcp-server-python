import requests

client_id = "testclient"
url = f"http://localhost:8001/api/send/{client_id}"
message = "Xin chao tu MCP Server"

response = requests.post(url, data=message)

print("Send status:", response.status_code)
print("Response:", response.json())
