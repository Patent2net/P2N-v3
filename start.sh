#!/bin/bash
source /vpy3/bin/activate
export PATH="$PATH:/vpy3/bin"
export FLASK_APP=app.py
flask run --host=0.0.0.0

