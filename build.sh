#!/bin/bash
# Arrêter le script si une commande échoue
set -e

# Afficher chaque commande avant de l'exécuter
set -x

# Installation des dépendances
echo "Installation des dépendances"
python3.12 -m pip install -r requirements.txt --break-system-packages

# Collecte des fichiers statiques
echo "Collection des fichiers statiques"
python3.12 manage.py collectstatic --noinput