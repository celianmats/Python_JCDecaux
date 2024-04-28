from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_bike_data(api_key):
    url = f"https://api.jcdecaux.com/vls/v1/contracts?apiKey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            bike_data = []
            for contract in data:
                contract_name = contract['name']
                commercial_name = contract['commercial_name']
                stations_url = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}"
                stations_response = requests.get(stations_url)
                if stations_response.status_code == 200:
                    stations_data = stations_response.json()
                    num_stations = len(stations_data)
                    bike_data.append({'contract_name': contract_name.capitalize(), 'commercial_name': commercial_name, 'num_stations': num_stations})
                else:
                    print(f"La demande des stations pour le contrat {contract_name} a échoué avec le code : {stations_response.status_code}")

            # Tri des contrats par nombre de stations (ordre décroissant)
            bike_data_sorted = sorted(bike_data, key=lambda x: x['num_stations'], reverse=True)

            return bike_data_sorted
        else:
            print(f"La demande à l'API a échoué avec le code : {response.status_code}")
            return None
    except Exception as e:
        print("Une erreur s'est produite lors de la récupération des données:", e)
        return None

def calculate_percentage_electric_stations(bike_data):
    total_stations = 0
    electric_stations = 0
    for contract in bike_data:
        num_stations = contract.get('num_stations', 0)
        total_stations += num_stations
        electric_stations += num_stations  # Supposons que toutes les stations sont électriques, sinon ajustez la logique ici

    if total_stations > 0:
        percentage_electric = (electric_stations / total_stations) * 100
        return percentage_electric
    else:
        return 0

@app.route('/')
def index():
    api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"
    bike_data = get_bike_data(api_key)
    if bike_data:
        percentage_electric = calculate_percentage_electric_stations(bike_data)
        if percentage_electric is not None:
            return render_template('index.html', percentage_electric=percentage_electric, bike_data=bike_data)
    return "Erreur lors de la récupération des données."

if __name__ == '__main__':
    app.run(debug=True)









