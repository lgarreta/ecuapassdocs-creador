#!/usr/bin/env python

"""
Remove old migrations and re-create django models
by makemigrations and migrations. Also add instances
to basic tables.
"""

# reinitialize database

import os
from django.core.management import call_command
from django.contrib.auth.models import User
from init_django import *

USER="admindb2"
PASSWORD="admindb2"
EMAIL="admindb2@gmail.com"
APPPATH="/home/lg/BIO/iaprojects/ecuapassdocs/ecuapassdocs-creador-dev/"

def printSettings ():
	print ("USER:", USER)
	print ("PATH:", APPPATH)

	if input ("Continuar reinicializando DB ? (YES/No") != "YES":
		sys.exit (0)

def remove_migrations ():
	a = input ("Remove migrations...")
	os.system ("rm appdocs/migrations/00*.py")
	os.system ("rm appusuarios/migrations/00*.py")

def reinitialize_database():
	a = input ("Reinitialize DB...")
    call_command('flush', '--noinput')

	a = input ("Makemigrations...")
    call_command('makemigrations')

	a = input ("Superuser...")
    call_command('migrate')

	user = User.objects.create_superuser(USER, EMAIL, PASSWORD)

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------
init_django_settings ()
os.chdir (APPPATH)

printSettings ()

remove_migrations ()

reinitialize_database ()

