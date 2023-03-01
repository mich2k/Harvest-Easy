#!/usr/bin/bash
# This script is run by the local boot process to start the Flask server
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
export HERE_KEY=XQlhgTyikHJMIi35pKcqjf3AbGBYho6FL8mvncE4T_g
export WEATHER_KEY=8db7edbf3f049e2543fb1115755351c0
export OPENROUTESERVICE_KEY='5b3ce3597851110001cf6248fc2f564415384fcead02c940fc913bb3'
export TOKEN='5887797061:AAEvYrnkdgFwS5nKmfoSJXNck-kzefUFEC0'
gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app