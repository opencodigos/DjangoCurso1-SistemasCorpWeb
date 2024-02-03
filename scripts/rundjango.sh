#!/bin/sh

set -e

# Espera db disponível antes de continuar a iniciar o aplicativo
python manage.py wait_for_db

python manage.py collectstatic --noinput

python manage.py migrate

# inicia uwsgi (EM FOREGROUND, melhor para uso em docker)
uwsgi --socket :9000 --workers 4 --master --enable-threads --module core.wsgi