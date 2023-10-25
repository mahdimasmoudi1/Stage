import serial
import requests
import time
import threading

# Créer un tableau pré-rempli avec des valeurs initiales
tableau = [
    ["0500", 0, 100,"0002","7107"],
    ["0502", 0, 100,"0002","D0C7"],
    ["0504", 0, 100,"0002","6408"],
    ["0506", 0, 100,"0002","7DC8"],
    ["0508", 0, 100,"0002","3408"],
    ["050A", 0, 100,"0002","2DC8"],
    ["050C", 0, 100,"0002","05C8"],
    ["050E", 0, 10000,"0002","10C4"],
    ["0510", 0, 10000,"0002","0408"],
    ["0512", 0, 10000,"0002","1DC8"],
    ["0514", 0, 10000,"0002","3103"],
    ["0516", 1, 1,"0002","90c3"],
    ["0518", 1, 1,"0002","f100"],
    ["051A", 1, 1,"0002","50c0"],
    ["051C", 1, 1,"0002","b0c1"],
    ["051E", 1, 1,"0002","1101"],
    ["0520", 1, 1,"0002","70cd"],
    ["0522", 1, 1,"0002","d10d"],
    ["0524", 1, 1,"0002","310c"],
    ["0526", 0, 1,"0002","90cc"],
    ["0528", 0, 1,"0002","f10f"],
    ["052A", 0, 1,"0002","50cf"],
    ["052C", 0, 1,"0002","b0ce"],
    ["052E", 0, 10000,"0001","510f"],
    ["052F", 0, 1,"0001","00cf"],
    ["0530", 0, 10000,"0001","3109"],
    ["0531", 0, 1,"0001","60c9"],
    ["0532", 0, 10000,"0001","90c9"],
    ["0533", 0, 1,"0001","c109"],
    ["0534", 0, 10000,"0001","70c8"],
    ["0535", 0, 1,"0001","2108"],
    ["0536", 0, 10000,"0001","d108"],
    ["0537", 0, 1,"0001","80c8"],
    ["0538", 0, 10000,"0001","b0cb"],
    ["0539", 0, 1,"0001","e10b"],
    ["053A", 0, 10000,"0001","110b"],
    ["053B", 0, 1,"0001","40cb"],
    ["053C", 0, 10000,"0001","f10a"],
    ["053D", 0, 1,"0001","a0ca"],
    ["053E", 0, 10000,"0001","50ca"],
    ["053F", 0, 10000,"0001","010a"],
    ["0540", 0, 10000,"0001","30d2"],
    ["0541", 0, 10000,"0001","6112"],
    ["0542", 0, 10000,"0001","9112"],
    ["0543", 0, 10000,"0001","c0d2"],
    ["0544", 0, 100,"0001","7113"],
    ["0545", 0, 100,"0001","20D3"],
    ["0546", 0, 10000,"0002","90d2"]
    # Ajoutez autant de lignes que nécessaire
]

# Configuration du port série
ser = serial.Serial('COM9', baudrate=38400, timeout=1)
# Configuration de l'URL de l'API Flask
api_url = "http://127.0.0.1:5002/receive-from-script"  # Changer l'URL si nécessaire


# Variable pour stocker les données reçues
received_data = ""
# Fonction pour lire les données série et les envoyer à l'API Flask
def read_and_send_data():
    global received_data
    try:
        while True:
            # Lire les données depuis le port série si nécessaire
            data = ser.read_until(b'\n')  # Lire jusqu'au prochain retour à la ligne (ou ajustez en fonction de votre format)
            
            if len (data) > 3 and data != "adresse introuvable" :
                print(data)
                # Convertir les données hexadécimales en bytes
                data_hex = data.hex()
                print(data_hex)
                if data_hex.startswith("0104"):
                    print("Received hexadecimal data from serial:", data_hex)
                        # Extraire le 5ème et le 6ème caractère de la chaîne
                    cinquieme_caractere = data_hex[4]
                    sixieme_caractere = data_hex[5]
                    nombre_str = cinquieme_caractere + sixieme_caractere
                    # Convertissez la chaîne en un entier
                    nb = int(nombre_str)
                    
                    data_str1 = data_hex[6:8]
                    data_str = data_hex[6:6+nb*2]
                    data_int1 = int(data_str1, 16)
                    data_int = int(data_str, 16)
                    correspondance_trouvee = False  # Ajoutez cette variable booléenne
                    for ligne in tableau:    
                        if ligne[0] == data_string1:
                            signe = ligne[1]
                            div = ligne[2]
                            if signe == 0:
                                data = data_int / div
                                print("signe0   :",data)
                            elif data_int1 < 127:
                                signed_data = data_int / div
                                data = signed_data
                                print("signe1   :",data)
                            else:
                                signed_data = 128 - (data_int - 128)
                                data = not signed_data / div
                                print("signe1+   :",data)
                            correspondance_trouvee = True  # Indiquez que la correspondance a été trouvée

                    if not correspondance_trouvee:  # Si aucune correspondance n'a été trouvée
                        data = "adresse introuvable"

                        
                    print("Données hexadécimales reçues:", data_hex)
                    print("5ème caractère:", cinquieme_caractere)
                    print("6ème caractère:", sixieme_caractere)
                    print("Données extraites:", data_str)
                    print("Données converties en entier:", data_int)
                    print(data)
                    # Envoyer les données à l'API Flask
                    response = requests.post(api_url, json={"data": data})
                    print("API response:", response.json())

                    # Stocker les données reçues
                    received_data = data_hex

            # Attendre un certain temps avant de lire à nouveau
            time.sleep(1)  # Attendre 1 seconde

    except KeyboardInterrupt:
        ser.close()
        print("Serial connection closed.")

# Lancer la fonction de lecture des données série dans un thread séparé
serial_thread = threading.Thread(target=read_and_send_data)
serial_thread.daemon = True
serial_thread.start()
data_string1 = ""  # Initialisez cette variable en dehors de la boucle
crc_value = None

while True:
    try:
        # Effectuer une requête GET pour récupérer les données de l'API Flask
        api_response = requests.get("http://127.0.0.1:5001/send-data")

        if api_response.status_code == 200:
            new_data_string1 = api_response.json().get('message')  # Extraire le message du dictionnaire
            if new_data_string1  != "" :
                print("Données reçues depuis l'API Flask:", new_data_string1)
                # Mettre à jour data_string1 uniquement si de nouvelles données sont disponibles
                data_string1 = new_data_string1
            if data_string1 != "" :
                print("Données reçues depuis l'API Flask:", data_string1)
            print(data_string1)

        # Vous pouvez maintenant utiliser data_string1 pour construire le message à envoyer au port série
        if data_string1 is not None:
            # Recherchez la taille correspondante dans le tableau
            taille = ""
            crc_value=""
            for ligne in tableau:
                if ligne[0] == data_string1:
                    taille = ligne[3]
                    crc_value = ligne[4]
                    break  # Sortez de la boucle dès que vous avez trouvé la correspondance

            if taille != "" and crc_value!= "" :
                # Construire la chaîne de données sans CRC pour le moment
                data_string = "0104" + data_string1 + taille + crc_value
                # Envoyer les données vers le port série
                ser.write(bytes.fromhex(data_string))
                print(f"Données envoyées : {data_string}")

        # Attendre un certain temps avant de faire la prochaine demande
        time.sleep(1)  # Attendre 5 secondes entre chaque demande

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Une erreur s'est produite :", str(e))

# Fermer le port série à la fin
ser.close()