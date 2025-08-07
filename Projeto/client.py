import requests

BASE_URL = "http://127.0.0.1:5000"

# 1️⃣ Criar uma URL encurtada
print("🔹 Criando URL encurtada...")
response = requests.post(f"{BASE_URL}/api/shorten", json={"url": "https://www.google.com"})
print(response.json())

short_id = response.json()["short_id"]

# 2️⃣ Buscar a URL original
print("\n🔹 Buscando URL original...")
response = requests.get(f"{BASE_URL}/api/{short_id}")
print(response.json())

# 3️⃣ Deletar a URL encurtada
print("\n🔹 Deletando URL encurtada...")
response = requests.delete(f"{BASE_URL}/api/{short_id}")
print(response.json())
