from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Utilisez un dictionnaire pour stocker les données reçues du script Python
received_data_from_script = {"data": None}
@app.route('/receive-from-script', methods=['POST'])
def receive_data_from_script():
    global received_data_from_script
    data= request.json.get('data')  # Récupérer les données depuis la requête JSON
    received_data_from_script["data"] = data
    print("Données reçues depuis le script Python:", data)
    return jsonify({"message": "Données reçues depuis le script Python"})

@app.route('/send-data-to-web', methods=['GET'])
def send_data_to_web():
    global received_data_from_script
    data = received_data_from_script["data"]
    if data:
        print(data)
        # Si des données ont été reçues depuis le script Python, renvoyez-les au site web
        return jsonify({"data": data})
    else:
        if data == 0:
            print("0.0")
            return jsonify({"data": "0.0"})
        else :
            print("no data")
        return jsonify({"message": ""})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)