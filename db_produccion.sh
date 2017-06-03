#!/bin/bash
# -*- ENCODING: UTF8 -*-

echo -e "Base de datos BD produccion"
echo -e "Borrando la base de datos."
dropdb -i --if-exists -U "$USER" polimbae_db_prod

if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos, verifique que nadie la este usando."
    exit 1
fi
echo -e "Se ha borrado BD produccion."
echo -e "Creando nueva BD produccion."
createdb -U "$USER" polimbae_db_prod
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear BD produccion"
    exit 2
fi
echo -e "Se ha creado BD produccion."


cd /home/"$USER"/produccion/PoliMbae
python manage.py makemigrations
python manage.py migrate
python poblacion.py

echo -e "BD produccion se cargo exitosamente."

