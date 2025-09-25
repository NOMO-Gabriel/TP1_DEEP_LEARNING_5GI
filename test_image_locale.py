# =====================================================================
# FICHIER : test_local_image.py
# Rôle : Envoyer une VRAIE image depuis le disque dur à l'API
# =====================================================================
import requests
from PIL import Image, ImageOps
import numpy as np

# --- 1. Préparer l'image locale ---
IMAGE_PATH = "mon_chiffre.png" # Mettez le nom de votre image ici

try:
    # Charger l'image
    img = Image.open(IMAGE_PATH)

    # Convertir en niveaux de gris
    img = img.convert('L')

    # Redimensionner en 28x28 pixels
    img = img.resize((28, 28))

    # Inverser les couleurs (chiffre blanc sur fond noir)
    img = ImageOps.invert(img)

    # Convertir l'image en tableau NumPy et l'aplatir en une liste
    image_array = np.array(img)
    image_payload = image_array.flatten().tolist()

    # --- 2. Envoyer la requête à l'API ---
    api_url = "http://localhost:5000/predict"
    payload = {"image": image_payload}

    print(f"Envoi de l'image '{IMAGE_PATH}' au serveur...")
    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    # --- 3. Afficher la réponse ---
    result = response.json()
    print("\nRéponse du serveur :")
    print(f"  Prédiction : {result['prediction']}")

except FileNotFoundError:
    print(f"Erreur : Le fichier '{IMAGE_PATH}' n'a pas été trouvé.")
    print("Veuillez créer une image de chiffre et la sauvegarder sous ce nom.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")