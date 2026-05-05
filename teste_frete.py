import requests

API_KEY = "AIzaSyDl7f3hRw-M1gXtdxhRhk9O3Ck05a3KSfw"

ORIGEM = "Av. Melvin Jones, 333, Ponta Grossa, PR"
DESTINO = "Rua Balduíno Taques, Ponta Grossa, PR"

def calcular_taxa(km):
    if km <= 1:
        return 5.25
    elif km <= 2:
        return 6.50
    elif km <= 3:
        return 7.50
    elif km <= 4:
        return 9.50
    elif km <= 6:
        return 11.50
    elif km <= 8:
        return 13.99
    elif km <= 10:
        return 16.50
    elif km <= 12:
        return 19.00
    elif km <= 15:
        return 24.90
    elif km <= 17:
        return 29.90
    elif km <= 20:
        return 35.00
    else:
        return None

url = "https://routes.googleapis.com/directions/v2:computeRoutes"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "routes.distanceMeters"
}

body = {
    "origin": {"address": ORIGEM},
    "destination": {"address": DESTINO},
    "travelMode": "DRIVE"
}

response = requests.post(url, json=body, headers=headers)
data = response.json()

if "routes" in data:
    distancia_metros = data["routes"][0]["distanceMeters"]
    distancia_km = distancia_metros / 1000

    taxa = calcular_taxa(distancia_km)

    print(f"Distância: {distancia_km:.2f} km")

    if taxa:
        print(f"Taxa de entrega: R$ {taxa:.2f}")
    else:
        print("Entrega sob consulta")
else:
    print("Erro:", data)