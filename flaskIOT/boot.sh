#!/bin/bash

source venv/bin/activate
#flask deploy
exec gunicorn -b :5000 --timeout 0 --access-logfile - --error-logfile - flasky:app