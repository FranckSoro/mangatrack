#!/bin/bash

set -e

python3.12 -m pip install -r requirements.txt --break-system-packages

curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

cd src/theme/static_src

npm install

cd ../../..

python3.12 src/manage.py tailwind build

python3.12 src/manage.py collectstatic --noinput