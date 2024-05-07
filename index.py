from flask import Flask, render_template, url_for
import requests

app = Flask(__name__)

def get_bike_data(api_key):
    # Fonction pour récupérer les données sur les contrats de vélos
    url = f"https://api.jcdecaux.com/vls/v1/contracts?apiKey={api_key}"
    try:
        # Envoie de la requête à l'API JCDecaux pour les contrats de vélos
        response = requests.get(url)
        # Vérification du statut de la réponse
        print(f"Statut de la réponse pour les contrats de vélos : {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            bike_data = []
            for contract in data:
                contract_name = contract['name']
                commercial_name = contract.get('commercial_name', '')
                # Construction de l'URL pour récupérer les stations pour ce contrat
                stations_url = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}"
                # Envoie de la requête pour récupérer les stations
                stations_response = requests.get(stations_url)
                # Vérification du statut de la réponse des stations
                print(f"Statut de la réponse pour les stations de {contract_name}: {stations_response.status_code}")
                if stations_response.status_code == 200:
                    stations_data = stations_response.json()
                    # Calcul du nombre de stations et du nombre total de vélos disponibles
                    num_stations = len(stations_data)
                    total_bikes = sum(station['available_bikes'] for station in stations_data)
                    # Calcul de la moyenne de vélos disponibles par station
                    avg_bikes_per_station = total_bikes / num_stations if num_stations > 0 else 0
                    # Ajout des données à la liste
                    bike_data.append({'contract_name': contract_name.capitalize(),
                                      'commercial_name': commercial_name,
                                      'num_stations': num_stations,
                                      'total_bikes': total_bikes,
                                      'avg_bikes_per_station': avg_bikes_per_station})
            # Tri des contrats par nombre de stations
            bike_data_sorted = sorted(bike_data, key=lambda x: x['num_stations'], reverse=True)
            return bike_data_sorted

        else:
            print(f"La demande à l'API a échoué : {response.status_code}")
            return None
    except Exception as e:
        print("Une erreur s'est produite lors de la récupération des données:", e)
        return None

@app.route('/')
def index():
    api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"
    bike_data = get_bike_data(api_key)

    # Vérification si les données ont été récupérées avec succès
    if bike_data:
        return render_template('index.html', bike_data=bike_data)
    return "Erreur lors de la récupération des données."

@app.route('/stations/<contract_name>')
def station_details(contract_name):
    api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"
    # Récupérer les détails des stations pour le contrat spécifié
    stations_url = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}"
    try:
        response = requests.get(stations_url)
        if response.status_code == 200:
            stations_data = response.json()
            return render_template('station_details.html', contract_name=contract_name, stations=stations_data)
        else:
            return f"Erreur lors de la récupération des données pour {contract_name}."
    except Exception as e:
        return f"Une erreur s'est produite : {e}"

if __name__ == '__main__':
    app.run(debug=True)












