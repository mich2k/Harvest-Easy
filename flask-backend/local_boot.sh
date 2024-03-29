#!/usr/bin/bash
# This script is run by the local boot process to start the Flask server

# DEPRECATED, use docker image instead!

DIR="venv"
if [ ! -d "$DIR" ]; then
  echo "Setting up venv in ${DIR}..."
  python3 -m venv $DIR
  source $DIR/bin/activate
  echo "Installing needed requirements..."
  $DIR/bin/pip3 install -r requirements.txt
  echo "Set up done"
else
  echo "Using existing venv in ${DIR}..."
  source $DIR/bin/activate
fi

export FLASK_CONFIG=local
export HERE_KEY=YOUR_KEY
export WEATHER_KEY=YOUR_KEY
export OPENROUTESERVICE_KEY=YOUR_KEY
export TOKEN='YOUR_KEY'
gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app