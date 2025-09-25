# =====================================================================
# FICHIER : test_client.py
# Rôle : Envoyer une image de test à notre API Flask
# =====================================================================
import requests
import numpy as np
from tensorflow import keras

# --- 1. Préparer une image de test ---
# On recharge le jeu de données MNIST pour avoir une image à envoyer
(_, _), (x_test, y_test) = keras.datasets.mnist.load_data()

# On prend la toute première image du jeu de test
image_index = 0
test_image = x_test[image_index]
true_label = y_test[image_index]

# On la prépare exactement comme dans le script d'entraînement
# Note : On n'a pas besoin de la normaliser ici, car l'API s'en charge
image_payload = test_image.flatten().tolist() # On la transforme en une simple liste

# --- 2. Envoyer la requête à l'API ---
api_url = "http://localhost:5000/predict"
payload = {"image": image_payload}

print(f"Envoi d'une image au serveur. La vraie valeur est : {true_label}")

try:
    response = requests.post(api_url, json=payload)
    response.raise_for_status() # Lève une exception si la requête a échoué

    # --- 3. Afficher la réponse du serveur ---
    result = response.json()
    print("\nRéponse du serveur :")
    print(f"  Prédiction : {result['prediction']}")
    
    # Afficher les 3 probabilités les plus élevées
    probabilities = result['probabilities'][0]
    top_3_indices = np.argsort(probabilities)[-3:][::-1]
    print("\n  Top 3 des probabilités :")
    for i in top_3_indices:
        print(f"    Chiffre {i}: {probabilities[i]*100:.2f}%")

except requests.exceptions.RequestException as e:
    print(f"\nErreur : Impossible de contacter le serveur à {api_url}.")
    print("Avez-vous bien lancé le serveur avec 'python app.py' ou 'docker run' ?")