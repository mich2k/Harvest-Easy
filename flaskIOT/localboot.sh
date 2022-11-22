#!/usr/bin/bash

# This script is run by the local boot process to start the Flask server

DIR="venv"

if [ ! -d "$DIR" ]; then
  echo "Setting up venv in ${DIR}..."
  python3 -m venv venv
  source venv/bin/activate
  echo "Installing needed requirements..."
  venv/bin/pip3 install -r requirements.txt
  echo "Set up done"
else
  echo "Using existing venv in ${DIR}..."
  source venv/bin/activate
fi

export FLASK_CONFIG=local

gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app
