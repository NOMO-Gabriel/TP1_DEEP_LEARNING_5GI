# =====================================================================
# FICHIER : train_model.py (Version avec MLflow)
# =====================================================================

import tensorflow as tf
from tensorflow import keras
import numpy as np
import mlflow  # <-- AJOUT 1 : Importer mlflow
import mlflow.tensorflow  # <-- AJOUT 2 : Importer le module pour tensorflow

# --- Variables pour les paramètres ---
# AJOUT 3 : Définir les hyperparamètres comme variables
EPOCHS = 5
BATCH_SIZE = 128
DROPOUT_RATE = 0.2

# Lancement de la session de suivi MLflow
# AJOUT 4 : Tout le processus est maintenant dans un bloc "with mlflow.start_run()"
with mlflow.start_run():
    
    # Enregistrement des paramètres
    mlflow.log_param("epochs", EPOCHS)
    mlflow.log_param("batch_size", BATCH_SIZE)
    mlflow.log_param("dropout_rate", DROPOUT_RATE)

    # 1. Chargement du jeu de données MNIST
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # 2. Normalisation des données
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    # 3. Redimensionnement des images
    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)

    # 4. Construction du modèle séquentiel
    model = keras.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        keras.layers.Dropout(DROPOUT_RATE),  # <-- Utiliser la variable
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
        epochs=EPOCHS,  # <-- Utiliser la variable
        batch_size=BATCH_SIZE,  # <-- Utiliser la variable
        validation_split=0.1
    )

    # 7. Évaluation du modèle sur les données de test
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f"Précision sur les données de test: {test_acc:.4f}")

    # Enregistrement des métriques
    # AJOUT 5 : Enregistrer la métrique de test
    mlflow.log_metric("test_accuracy", test_acc)
    mlflow.log_metric("test_loss", test_loss)

    # Enregistrement du modèle complet
    # AJOUT 6 : Enregistrer le modèle comme un "artefact"
    mlflow.keras.log_model(model, "mnist-model")

    print("Modèle, paramètres et métriques enregistrés avec MLflow.")

# La sauvegarde manuelle n'est plus nécessaire car MLflow s'en charge
# model.save("mnist_model.h5")
# print("Modèle sauvegardé sous le nom mnist_model.h5")