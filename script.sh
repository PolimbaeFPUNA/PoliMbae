#!/bin/bash

source /home/ivan/dev/venv/bin/activate
cd /home/ivan/dev/PoliMbae

cd /home/ivan/dev/PoliMbae
chmod +x db_desarrollo.sh
./db_desarrollo.sh
cd /home/ivan/dev/PoliMbae
python manage.py runserver&
sleep 2
xdg-open http://localhost:8000/grafico/recursos


