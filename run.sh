#!/bin/sh
pip install -r requirements.txt

python ccoins_fetch_srv.py runserver --host=127.0.0.1 --port=5000 -d