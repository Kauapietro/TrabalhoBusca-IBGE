from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_cities_ordered_by_state():
    response_states = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    states = response_states.json()
    cities_by_state = {}

    for state in states:
        response_cities = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state['sigla']}/municipios")
        cities = response_cities.json()
        city_names = sorted([city['nome'] for city in cities])

        cities_by_state[state['sigla']] = city_names

    return cities_by_state

@app.route('/')
def index():
    return "Acesse /cities para visualizar os nomes das cidades agrupados por estado. Use /cities/<estado> para ver as cidades de um estado específico."

@app.route('/cities')
def get_all_cities():
    cities_by_state = get_cities_ordered_by_state()
    return jsonify(cities_by_state)

@app.route('/cities/<state>')
def get_cities_by_state(state):
    cities_by_state = get_cities_ordered_by_state()
    if state.upper() in cities_by_state:
        return jsonify({state.upper(): cities_by_state[state.upper()]})
    else:
        return jsonify({"error": "Estado não encontrado."}), 404

if __name__ == '__main__':
    app.run(debug=True)
