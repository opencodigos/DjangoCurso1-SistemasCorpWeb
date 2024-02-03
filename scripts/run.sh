#!/bin/sh

set -e -x

echo "$@"

chown -R app:app /vol
chown -R app:app /vol/web

ls -la /vol/
ls -la /vol/web
ls -la /scripts/

su-exec app rundjango.sh