
from flask import Flask, request, jsonify, send_from_directory
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

plantas = [
    {"nome": "Spider Plant", "luz": "low,medium,bright", "rega": 1, "cuidado": "Easy", "segura": False, "altura": 45, "porte": "small", "umidade": "any", "imagem": "imagens/spider-plant.jpg", "descricao": "A resilient plant with arching leaves; keep it away from pets that may chew plants."},
    {"nome": "Calathea", "luz": "low,medium", "rega": 2, "cuidado": "Medium", "segura": True, "altura": 60, "porte": "small", "umidade": "humid", "imagem": "imagens/Calathea.jpg", "descricao": "Decorative patterned leaves; prefers consistent moisture and higher humidity."},
    {"nome": "Snake Plant", "luz": "low,medium,bright", "rega": 1, "cuidado": "Easy", "segura": False, "altura": 90, "porte": "large", "umidade": "any", "imagem": "imagens/Snake Plant.webp", "descricao": "Upright leaves and drought tolerance; keep away from pets."},
    {"nome": "Areca Palm", "luz": "bright,medium", "rega": 2, "cuidado": "Medium", "segura": True, "altura": 180, "porte": "large", "umidade": "humid", "imagem": "imagens/Areca Palm.webp", "descricao": "A leafy plant that enjoys bright indirect light and room to grow."},
    {"nome": "Pothos", "luz": "low,medium,bright", "rega": 1, "cuidado": "Easy", "segura": False, "altura": 120, "porte": "large", "umidade": "any", "imagem": "imagens/Pothos.jpg", "descricao": "A trailing plant that adapts to many indoor spaces; keep away from pets."},
    {"nome": "Parlor Palm", "luz": "low,medium", "rega": 1, "cuidado": "Easy", "segura": True, "altura": 100, "porte": "large", "umidade": "any", "imagem": "imagens/Parlor Palm.jpg", "descricao": "A compact palm that can grow in lower light and is listed as pet-safe."},
    {"nome": "Fiddle-leaf Fig", "luz": "bright", "rega": 1, "cuidado": "Hard", "segura": False, "altura": 200, "porte": "large", "umidade": "any", "imagem": "imagens/Fiddle-leaf Fig.jpg", "descricao": "A tall decorative plant that needs a bright spot and careful watering."},
    {"nome": "Boston Fern", "luz": "medium", "rega": 3, "cuidado": "Medium", "segura": True, "altura": 75, "porte": "large", "umidade": "humid", "imagem": "imagens/Boston Fern.jpg", "descricao": "A lush fern that prefers moist soil and humid air."},
    {"nome": "Aloe Vera", "luz": "bright,direct", "rega": 1, "cuidado": "Easy", "segura": False, "altura": 50, "porte": "small", "umidade": "dry", "imagem": "imagens/Aloe Vera.jpg", "descricao": "A succulent that likes bright light and dry soil between waterings."},
    {"nome": "Peperomia", "luz": "medium,bright", "rega": 1, "cuidado": "Easy", "segura": True, "altura": 35, "porte": "small", "umidade": "any", "imagem": "imagens/Peperomia.webp", "descricao": "A compact plant with low watering needs and varied leaf shapes."}
]


@app.route("/")
def inicio():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/recomendar", methods=["POST"])
def recomendar():
    dados = request.get_json()

    luz = dados.get("luz")
    pets = dados.get("pets")
    experiencia = dados.get("experiencia")
    umidade = dados.get("umidade")
    rega = dados.get("rega")
    espaco = dados.get("espaco")
    temperatura = dados.get("temperatura")

    def combina(planta):
        return (
            luz in planta["luz"].split(",") and
            (not pets or planta["segura"]) and
            (experiencia != "beginner" or planta["cuidado"] == "Easy") and
            (umidade == "any" or planta["umidade"] == "any" or planta["umidade"] == umidade) and
            (rega == "any" or (rega == "low" and planta["rega"] <= 1) or (rega == "high" and planta["rega"] >= 2)) and
            (espaco == "any" or planta["porte"] == espaco)
        )

    lista = [planta for planta in plantas if combina(planta)]

    if not lista:
        lista = [
            planta for planta in plantas
            if luz in planta["luz"].split(",")
            and (not pets or planta["segura"])
            and (experiencia != "beginner" or planta["cuidado"] == "Easy")
        ]

    if not lista:
        return jsonify({"erro": "No plant found for these light and pet conditions."}), 404

    planta = random.choice(lista)

    motivo = "This plant can tolerate the light conditions you selected."

    if pets:
        motivo += " It is listed as pet-safe in our catalog."

    if experiencia == "beginner" and planta["cuidado"] == "Easy":
        motivo += " It is easy to care for."

    if umidade != "any" and (planta["umidade"] == umidade or planta["umidade"] == "any"):
        motivo += " It matches your humidity preference."

    if rega == "low" and planta["rega"] <= 1:
        motivo += " It needs less frequent watering."

    if rega == "high" and planta["rega"] >= 2:
        motivo += " It matches your preference for more frequent watering."

    if espaco != "any" and planta["porte"] == espaco:
        motivo += " Its size fits your space."

    if temperatura != "any":
        motivo += " Avoid extreme temperatures."

    resultado = planta.copy()
    resultado["motivo"] = motivo

    return jsonify(resultado)


@app.route("/<path:arquivo>")
def arquivos(arquivo):
    return send_from_directory(BASE_DIR, arquivo)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
