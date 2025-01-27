#!/bin/bash

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Compresser les fichiers statiques
python manage.py compress --force