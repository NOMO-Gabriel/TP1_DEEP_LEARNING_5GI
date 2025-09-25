# =====================================================================
# FICHIER : Dockerfile
# =====================================================================

# 1. Utiliser une image de base Python
FROM python:3.9-slim

# 2. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 3. Copier le fichier des dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le reste de l'application (le code et le modèle)
COPY . .

# 5. Exposer le port que l'application Flask utilise
EXPOSE 5000

# 6. Commande pour démarrer l'application lorsque le conteneur se lance
CMD ["python", "app.py"]