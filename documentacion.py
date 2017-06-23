import django
import pydoc
import os
os.environ['DJANGO_SETTINGS_MODULE']="PoliMbae.settings"
django.setup()
pydoc.writedocs('/home/ivan/dev/PoliMbae')
