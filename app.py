from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "AIzaSyDl7f3hRw-M1gXtdxhRhk9O3Ck05a3KSfw"
ORIGEM = "Av. Melvin Jones, 333, Ponta Grossa, PR, Brasil"


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


def calcular_distancia(destino):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters"
    }

    body = {
        "origin": {"address": ORIGEM},
        "destination": {"address": destino},
        "travelMode": "DRIVE"
    }

    response = requests.post(url, json=body, headers=headers, timeout=15)
    data = response.json()

    print("STATUS GOOGLE:", response.status_code)
    print("RESPOSTA GOOGLE:", data)

    if response.status_code != 200:
        return None, data

    if "routes" not in data or len(data["routes"]) == 0:
        return None, data

    km = data["routes"][0]["distanceMeters"] / 1000
    return km, None


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None

    if request.method == "POST":
        rua = request.form.get("rua", "").strip()
        numero = request.form.get("numero", "").strip()
        bairro = request.form.get("bairro", "").strip()

        if not rua or not numero or not bairro:
            erro = "Preencha rua, número e bairro."
        else:
            destino = f"{rua}, {numero}, {bairro}, Ponta Grossa, PR, Brasil"
            km, erro_google = calcular_distancia(destino)

            if km is None:
                erro = "Não foi possível calcular a distância."
            else:
                taxa = calcular_taxa(km)
                resultado = {
                    "endereco": destino,
                    "km": round(km, 2),
                    "taxa": taxa
                }

    return render_template("index.html", resultado=resultado, erro=erro)


@app.route("/frete", methods=["POST"])
def frete():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "success": False,
            "error": "Nenhum JSON recebido."
        }), 400

    rua = str(dados.get("rua", "")).strip()
    numero = str(dados.get("numero", "")).strip()
    bairro = str(dados.get("bairro", "")).strip()
    cidade = str(dados.get("cidade", "Ponta Grossa")).strip()
    estado = str(dados.get("estado", "PR")).strip()

    if not rua or not numero or not bairro:
        return jsonify({
            "success": False,
            "error": "Informe rua, número e bairro."
        }), 400

    destino = f"{rua}, {numero}, {bairro}, {cidade}, {estado}, Brasil"

    km, erro_google = calcular_distancia(destino)

    if km is None:
        return jsonify({
            "success": False,
            "error": "Não foi possível calcular a distância.",
            "google_error": erro_google
        }), 400

    taxa = calcular_taxa(km)

    if taxa is None:
        return jsonify({
            "success": False,
            "error": "Endereço acima de 20km. Entrega sob consulta.",
            "km": round(km, 2)
        }), 200

    return jsonify({
        "success": True,
        "origem": ORIGEM,
        "destino": destino,
        "km": round(km, 2),
        "taxa": round(taxa, 2)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)