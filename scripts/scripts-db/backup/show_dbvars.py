#!/usr/bin/env python

from django.conf import settings
from init_django import *

def get_current_database_settings():
    default_db = settings.DATABASES['default']
    return {
        'ENGINE': default_db['ENGINE'],
        'NAME': default_db['NAME'],
        'USER': default_db['USER'],
        'PASSWORD': default_db['PASSWORD'],
        'HOST': default_db['HOST'],
        'PORT': default_db['PORT'],
    }

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------
init_django_settings ()
current_database_settings = get_current_database_settings()
for k in current_database_settings.keys():
	print (f"{k} : {current_database_settings [k]}")

