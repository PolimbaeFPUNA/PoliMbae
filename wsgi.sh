#!/bin/bash

cd /home/"$USER"/produccion
touch PoliMbae.conf
chmod 777 PoliMbae.conf
echo listen 9090 >>PoliMbae.conf
echo \<VirtualHost *:9090\> >>PoliMbae.conf
echo 		 >>PoliMbae.conf
echo      >>PoliMbae.conf
echo   \<Directory /home/"$USER"/produccion/PoliMbae\> >>PoliMbae.conf 
echo     \<Files wsgi.py\> >>PoliMbae.conf
echo       Require all granted >>PoliMbae.conf
echo     \</Files\> >>PoliMbae.conf
echo   \</Directory\> >>PoliMbae.conf
echo   ServerName PoliMbae >>PoliMbae.conf
echo   ServerAdmin email@deladministrador.com >>PoliMbae.conf
echo   DocumentRoot /home/"$USER"/produccion/PoliMbae/ >>PoliMbae.conf
echo 	 >>PoliMbae.conf
echo   WSGIPassAuthorization On >>PoliMbae.conf
echo     >>PoliMbae.conf
echo   WSGIScriptAlias / /home/"$USER"/produccion/PoliMbae/PoliMbae/wsgi.py >>PoliMbae.conf
echo     >>PoliMbae.conf
echo   WSGIDaemonProcess PoliMbae python-path=/home/"$USER"/produccion/PoliMbae:/home/"$USER"/produccion/venv/lib/python2.7/site-packages >>PoliMbae.conf
echo  >>PoliMbae.conf
echo   Alias /static/ /home/"$USER"/produccion/PoliMbae/static/ >>PoliMbae.conf
echo   \<Directory /home/"$USER"/produccion/PoliMbae/static\> >>PoliMbae.conf
echo     Require all granted >>PoliMbae.conf
echo   \</Directory\> >>PoliMbae.conf
echo 	 >>PoliMbae.conf
echo   WSGIProcessGroup PoliMbae>>PoliMbae.conf
echo  >>PoliMbae.conf
echo \</VirtualHost\> >>PoliMbae.conf

cd /etc/apache2/sites-available

sudo rm PoliMbae.conf
sudo mv /home/"$USER"/produccion/PoliMbae.conf /etc/apache2/sites-available/

cd /home/"$USER"/produccion/PoliMbae/PoliMbae
rm wsgi.py
touch wsgi.py
echo import os, sys >> wsgi.py
echo   >> wsgi.py
echo sys.path.append\(\'/home/"$USER"/produccion/PoliMbae\'\)  >> wsgi.py
echo from django.core.wsgi import get_wsgi_application  >> wsgi.py
echo os.environ[\'DJANGO_SETTINGS_MODULE\']=\"PoliMbae.settings\"  >> wsgi.py
echo activate_this=\'/home/"$USER"/produccion/venv/bin/activate_this.py\'  >> wsgi.py
echo execfile\(activate_this,dict\(__file__=activate_this\)\)  >> wsgi.py
echo application = get_wsgi_application\(\)  >> wsgi.py


