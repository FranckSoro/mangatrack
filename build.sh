#!/bin/bash
# Arrêter le script si une commande échoue
set -e

# Afficher chaque commande avant de l'exécuter
set -x

echo "Installation de pip"
python3.12 -m ensurepip --upgrade

# Installation des dépendances
echo "Installation des dépendances"
python3.12 -m pip install -r requirements.txt

# Collecte des fichiers statiques
echo "Collection des fichiers statiques"
python3.12 manage.py collectstatic --noinput