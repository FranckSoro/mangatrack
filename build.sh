#!/bin/bash

set -e
set -x

echo "Installation des dépendances"
python3.12 -m pip install -r requirements.txt --break-system-packages

echo "Build Tailwind"
python3.12 src/manage.py tailwind build

echo "Collection des fichiers statiques"
python3.12 src/manage.py collectstatic --noinput