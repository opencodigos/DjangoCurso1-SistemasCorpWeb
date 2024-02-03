#!/bin/sh

set -e

# Printa as variaveis para ver o valor delas se está passando
echo "LISTEN_PORT=${LISTEN_PORT}"
echo "APP_HOST=${APP_HOST}"
echo "APP_PORT=${APP_PORT}"


# envsubst É uma ferramenta que substitui variáveis de ambiente em arquivos de texto
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# nginx  Inicia o servidor web Nginx.
# -g 'daemon off;' Configura o Nginx para não rodar como um daemon (em primeiro plano)
nginx -g 'daemon off;'