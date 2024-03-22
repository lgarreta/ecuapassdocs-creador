#!/usr/bin/env python
import os, sys

import django
from django.db import connection

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "appdocs_main.settings") #appdocs_main") #/settings")
sys.path.append (f"{os.getcwd()}")
django.setup ()

from appdocs.models import Cartaporte, CartaporteDoc, Manifiesto, ManifiestoDoc, Vehiculo, Conductor

def reinitialize_table_model (DocumentClass, DocumentFormClass):
	# Step 1: Delete all rows
	DocumentClass.objects.all().delete()
	DocumentFormClass.objects.all().delete()

	# Step 2: Reset auto-incrementing primary key (for PostgreSQL)
	if connection.vendor == 'postgresql':
		with connection.cursor() as cursor:
			if (DocumentClass == Cartaporte):
				print ("-- Deleting cartaportes...")
				cursor.execute ("ALTER SEQUENCE appdocs_cartaportedoc_id_seq RESTART WITH 1;")
				cursor.execute ("ALTER SEQUENCE appdocs_cartaporte_id_seq RESTART WITH 1;")
			elif (DocumentClass == Manifiesto):
				print ("-- Deleting manifiestos...")
				cursor.execute ("ALTER SEQUENCE appdocs_manifiestodoc_id_seq RESTART WITH 1;")
				cursor.execute ("ALTER SEQUENCE appdocs_manifiesto_id_seq RESTART WITH 1;")
			else:
				print (f"ALERTA: Tipo documento '{type (DocumentClass)}' no existente")

	# You may need to add similar code for other database backends if you're not using PostgreSQL

# Call the function to reinitialize the table model
reinitialize_table_model (Cartaporte, CartaporteDoc)
reinitialize_table_model (Manifiesto, ManifiestoDoc)

