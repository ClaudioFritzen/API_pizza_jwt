import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3IiwiZXhwIjoxNzU2MjI2MjMyLCJpYXQiOjE3NTU2MjE0MzJ9.oe3dW2bE6tT0fZEz39HVjIOS4Kd3Kn57KYkVwj7fTtI"
headers = {
    "Authorization": f"Bearer {token}"
}
requisicao = requests.get("http://localhost:8000/auth/refresh", headers=headers)

print(requisicao.status_code)
print(requisicao)
print(requisicao.json())