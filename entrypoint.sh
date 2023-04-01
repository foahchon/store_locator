#!/usr/bin/env bash

python3 -m flask db upgrade
python -m gunicorn --bind 0.0.0.0:80 'wsgi:app'