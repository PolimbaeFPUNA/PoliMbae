#!/bin/bash
# -*- ENCODING: UTF8 -*-

echo -e "Base de datos BD_Desarrollo"
echo -e "Borrando la base de datos."
dropdb -i --if-exists -U "$USER" polimbae_db

if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos, verifique que nadie la este usando."
    exit 1
fi
echo -e "Se ha borrado BD Desarrollo."
echo -e "Creando nueva BD Desarrollo."
createdb -U "$USER" polimbae_db
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear BD_Desarrollo"
    exit 2
fi
echo -e "Se ha creado BD_Desarrollo."


cd /home/"$USER"/dev/PoliMbae
python manage.py makemigrations
python manage.py migrate
python poblacion_desarrollo.py

echo -e "BD_Desarrollo se cargo exitosamente."

