#!/bin/bash

# Créer le dossier staticfiles s'il n'existe pas
mkdir -p staticfiles

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Compresser les fichiers statiques
python manage.py compress --force