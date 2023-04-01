#!/usr/bin/env bash

python3 -m flask db upgrade
python -m gunicorn 'wsgi:app'