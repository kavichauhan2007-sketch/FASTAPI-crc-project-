import requests

# 1. POST
data = {
    "title": "My Wallet",
    "description": "Black leather wallet",
    "category": "Accessories",
    "location": "Library",
    "reported_by": "John Doe",
    "status": "Lost"
}
response = requests.post("http://127.0.0.1:8000/items", json=data)
print("POST /items ->", response.status_code, response.text)

# 2. GET
response = requests.get("http://127.0.0.1:8000/items")
print("GET /items ->", response.status_code, response.text)
