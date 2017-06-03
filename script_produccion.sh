#!/bin/bash
cd /home/"$USER"
mkdir produccion
cd /home/"$USER"/produccion
virtualenv venv

source /home/"$USER"/produccion/venv/bin/activate
pip install django==1.10
pip install psycopg2

git clone https://github.com/PolimbaeFPUNA/PoliMbae.git

cd /home/"$USER"/produccion/PoliMbae/PoliMbae
sed -i 's/polimbae_db/polimbae_db_prod/g' "settings.py"
cd /home/"$USER"/produccion/PoliMbae
chmod +x db_produccion.sh
chmod +x wsgi.sh
./wsgi.sh
./db_produccion.sh
cd /home/"$USER"/produccion/PoliMbae
cp /home/"$USER"/dev/PoliMbae/poblacion.py /home/"$USER"/produccion/PoliMbae/poblacion.py 
python poblacion.py
sudo a2ensite PoliMbae.conf
sudo apache2ctl restart

sleep 2
xdg-open http://localhost:9090/grafico/recursos

