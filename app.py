# =====================================================================
# FICHIER : app.py
# =====================================================================
from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Initialiser l'application Flask
app = Flask(__name__)

# Charger le modèle Keras pré-entraîné
# Assurez-vous que le fichier mnist_model.h5 est dans le même répertoire
try:
    model = keras.models.load_model('mnist_model.h5')
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
    model = None

# Définir la route de prédiction
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Modèle non chargé'}), 500

    # Récupérer les données JSON de la requête
    data = request.json
    
    # Vérification des données d'entrée
    if 'image' not in data:
        return jsonify({'error': 'Aucune image fournie'}), 400
    
    try:
        # Convertir l'image en tableau NumPy
        image_data = np.array(data['image'])
        
        # Assurer le bon format (1, 784) et la normalisation
        image_data = image_data.reshape(1, 784)
        image_data = image_data.astype("float32") / 255.0
        
        # Faire la prédiction
        prediction = model.predict(image_data)
        predicted_class = np.argmax(prediction, axis=1)[0]
        
        # Renvoyer le résultat en JSON
        return jsonify({
            'prediction': int(predicted_class),
            'probabilities': prediction.tolist()
        })
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la prédiction : {e}'}), 400

# Lancer l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)