from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

received_data = None  # Utilisez une variable pour stocker les données reçues

@app.route('/receive-data', methods=['POST'])
def receive_data():
    global received_data
    data = request.json.get('data')  # Récupérer les données depuis la requête JSON

    # Traitez les données ici (vous pouvez les enregistrer en base de données, etc.)
    # Par exemple, stockez les données dans la variable received_data
    received_data = data

    print("Données reçues:", data)
    return jsonify({"message": "Données reçues avec succès"})

@app.route('/send-data', methods=['GET'])
def send_data():
    global received_data
    if received_data:
        # Si des données ont été reçues et stockées, renvoyez-les dans un dictionnaire JSON valide
        data_to_send = {"message": received_data}  # Utilisez une clé "message" pour encapsuler les données
        types = {"message1": data_to_send["message"][4:8]}  # Exemple de données dans types
        received_data = None  # Réinitialisez les données après l'envoi des données
        
        # Créez un dictionnaire qui contient à la fois data_to_send et types
        combined_data = {**data_to_send, **types}
        
        return jsonify(combined_data)
    else:
        return jsonify({"message": ""})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
