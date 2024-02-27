#!/usr/bin/env python

import os
from traceback import format_exc

import psycopg2
from psycopg2 import sql

a = input ("Remove migrations...")
os.system ("rm appdocs/migrations/00*.py")
os.system ("rm appusuarios/migrations/00*.py")

a = input ("Makemigrations...")
os.system ("python manage.py makemigrations")

a = input ("Migrate...")
os.system ("python manage.py migrate")

a = input ("Superuser...")
os.system ("python manage.py createsuperuser ")

# PostgreSQL database connection parameters
# Local posgress DB
db_params= {
    'dbname': 'ecuapassdocsdb',
    'user': 'admindb',
    'password': 'admindb2024A.',
    'host': 'localhost',
    'port': '5433',
}
"""

# Railway
#db_params= {
#	'dbname'  : os.environ.get ('PGDATABASE'),
#	'user'	  : os.environ.get ('PGUSER'),
#	'password': os.environ.get ('PGPASSWORD'),
#	'host'	  : os.environ.get ('PGHOST'),
#	'port'	  : os.environ.get ('PGPORT'),
#}

# Data to insert
#data = [
#    {'field1': 'value1', 'field2': 'value2'},
#    {'field1': 'value3', 'field2': 'value4'},
#    # Add more data as needed
#]
"""

def execute_sql_query(query, values=None):
    conn = psycopg2.connect(**db_params)
    with conn.cursor() as cursor:
        cursor.execute(query, values)
    conn.commit()
    conn.close()

#--------------------------------------------------------------------    
#-- Vehiculos
#--------------------------------------------------------------------    
vehiculos_data = [
    (1001, 'PNA12A', "CHEVROLET", "COLOMBIA", "1020", "2000"),
    (1002, 'PNB12B', "MAZDA", "ECUADOR", "1030", "1999"),
    (1003, 'PNC12C', "RENAULT", "ECUADOR", "1040", "1995")
]

empresas_data = [
    (1001, '1020', "CHEVROLET S.A", "AV. COLON", "CALI", "COLOMBIA", "NIT"),
    (1002, '1030', "MAZDA S.A.", "AV. RIO", "IBARRA",  "ECUADOR", "RUC"),
    (1003, '1040', "RENAULT S.A.", "AV. CIRC", "QUITO", "ECUADOR", "RUC")
]

conductores_data = [
    (1001, '11020', "JAIRO MORA", "COLOMBIA", "1102011", "1990-10-25"),
    (1002, '11030', "LUIS GARRETA", "ECUADOR", "1103011", "1990-12-31"),
    (1003, '11040', "ALFREDO DIAZ", "COLOMBIA", "1104011", "2000-05-22")
]


def populate_database (data, table):
	try:
		for entry in data:
			query = sql.SQL(f"INSERT INTO {table} VALUES {entry};")
				#sql.SQL(', ').join(map(sql.Identifier, entry.keys())),
				#sql.SQL(', ').join(map(sql.Placeholder, entry.values()))
			#)
			print (">>> query:", query)
			execute_sql_query(query)
	except:
		print (">>> Registro existente:", table, data)

if __name__ == '__main__':
    populate_database (vehiculos_data, "appdocs_vehiculo")
    populate_database (empresas_data, "appdocs_empresa")
    populate_database (conductores_data, "appdocs_conductor")
