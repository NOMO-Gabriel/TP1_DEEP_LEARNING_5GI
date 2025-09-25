# =====================================================================
# FICHIER : train_model.py (Version corrigée)
# =====================================================================

import tensorflow as tf
from tensorflow import keras
import numpy as np

# 1. Chargement du jeu de données MNIST
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 2. Normalisation des données
# On divise par 255 pour ramener les valeurs des pixels entre 0 et 1
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# 3. Redimensionnement des images
# On transforme chaque image de 28x28 pixels en un vecteur de 784 pixels
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)

# 4. Construction du modèle séquentiel
model = keras.Sequential([
    # Couche d'entrée et première couche cachée (512 neurones)
    keras.layers.Dense(512, activation='relu', input_shape=(784,)),
    # Couche de régularisation pour éviter le sur-apprentissage
    keras.layers.Dropout(0.2),
    # Couche de sortie (10 neurones, un par chiffre)
    keras.layers.Dense(10, activation='softmax')
])

# 5. Compilation du modèle
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 6. Entraînement du modèle
history = model.fit(
    x_train,
    y_train,
    epochs=5,
    batch_size=128,
    validation_split=0.1
)

# 7. Évaluation du modèle sur les données de test
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Précision sur les données de test: {test_acc:.4f}")

# 8. Sauvegarde du modèle entraîné
model.save("mnist_model.h5")
print("Modèle sauvegardé sous le nom mnist_model.h5")