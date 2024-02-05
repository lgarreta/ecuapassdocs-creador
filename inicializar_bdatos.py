#!/usr/bin/env python
import os
from traceback import format_exc
import sqlite3
import psycopg2

#from psycopg2 import sql

"""
a = input ("Remove sqlite...")
os.system ("rm db.sqlite3")
os.system ("rm appdocs/migrations/00*.py")

a = input ("Makemigrations...")
os.system ("python manage.py makemigrations")

a = input ("Migrate...")
os.system ("python manage.py migrate")

a = input ("Superuser...")
os.system ("python manage.py createsuperuser ")


# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('db.sqlite3')
# Create a cursor object to interact with the database
cursor = conn.cursor()
"""

# Local posgress DB
db_params= {
    'dbname': 'ecuapassdocsdb',
    'user': 'lg',
    'password': 'lge',
    'host': 'localhost',
    'port': '5432',
}

# Create a cursor object to interact with the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

a = input ("Data...")
# Insert data into the table

#--------------------------------------------------------------------    
#-- Vehiculos
#--------------------------------------------------------------------    
vehiculos_data = [
    (1, 'PNA12A', "CHEVROLET", "COLOMBIA", "1020", "2000"),
    (2, 'PNB12B', "MAZDA", "ECUADOR", "1030", "1999"),
    (3, 'PNC12C', "RENAULT", "ECUADOR", "1040", "1995")
]

try:
    cursor.executemany('''
                INSERT INTO appdocs_vehiculo (id, placa, marca, pais, chasis, anho)
                VALUES (?, ?, ?, ?, ?, ?) ''', vehiculos_data)
except:
    print ("Datos vehiculos ya existen")



#--------------------------------------------------------------------    
#-- Empresas
#--------------------------------------------------------------------    
empresas_data = [
    (1, '1020', "CHEVROLET S.A", "AV. COLON", "CALI", "COLOMBIA", "NIT"),
    (2, '1030', "MAZDA S.A.", "AV. RIO", "IBARRA",  "ECUADOR", "RUC"),
    (3, '1040', "RENAULT S.A.", "AV. CIRC", "QUITO", "ECUADOR", "RUC")
]

try:
    cursor.executemany('''
                INSERT INTO appdocs_empresa (id, numeroId, nombre, direccion, ciudad, pais, tipoId)
                VALUES (?, ?, ?, ?, ?, ?, ?) ''', empresas_data)
except:
    print ("Datos Empresas ya existen")

#--------------------------------------------------------------------    
#-- Conductores
#--------------------------------------------------------------------    
conductores_data = [
    (1, '11020', "JAIRO MORA", "COLOMBIA", "1102011", "1990-10-25"),
    (2, '11030', "LUIS GARRETA", "ECUADOR", "1103011", "1990-12-31"),
    (3, '11040', "ALFREDO DIAZ", "COLOMBIA", "1104011", "2000-05-22")
]

try:
    cursor.executemany('''
                INSERT INTO appdocs_conductor (id, documento, nombre, nacionalidad, licencia, fecha_nacimiento)
                VALUES (?, ?, ?, ?, ?, ?) ''', conductores_data)
except:
    print (format_exc())
    print ("Datos Conductores ya existen")


#--------------------------------------------------------------------    
#-- Cartaportes Doc
#--------------------------------------------------------------------    

cartaportesDoc_data = [
    (1, 'CO1020', "Texto 2" ),
    (2, 'CO1030', "Texto 22"),
    (3, 'CO1040', "Texto 222")
]
try:
    cursor.executemany('''
                INSERT INTO appdocs_cartaportedoc (id, numero, txt02)
                VALUES (?, ?, ?) ''', cartaportesDoc_data) 
except:
    #print (format_exc())
    print ("Datos Cartaportes Doc ya existen")

#--------------------------------------------------------------------    
#-- Cartaportes
#--------------------------------------------------------------------    
cartaportes_data = [
    (1, 'CPI1020', 1, 1, "2024-01-28"),
    (2, 'CPI1030', 2, 2, "2024-01-29"),
    (3, 'CPI1040', 3, 3, "2024-01-27")
]

try:
    cursor.executemany('''
                INSERT INTO appdocs_cartaporte (id, numero, remitente_id, documento_id, fecha_emision)
                VALUES (?, ?, ?, ?, ?) ''', cartaportes_data) 
except:
    print (format_exc())
    print ("Datos Cartaportes ya existen")

#--------------------------------------------------------------------    
#-- Manifiestos Doc
#--------------------------------------------------------------------    
manifiestosDoc_data = [
    (1, 'MCI1020', "Texto 3" ),
    (2, 'MCI1030', "Texto 33"),
    (3, 'MCI1040', "Texto 333")
]
try:
    cursor.executemany('''
                INSERT INTO appdocs_manifiestodoc (id, numero, txt02)
                VALUES (?, ?, ?) ''', manifiestosDoc_data) 
except:
    print (format_exc())
    print ("Datos Manifiestos Doc ya existen")

#--------------------------------------------------------------------    
#-- Manifiestos
#--------------------------------------------------------------------    
manifiestos_data = [
    (1, 'MCI1020',1, 1, "2024-01-28"),
    (2, 'MCI1030',2, 2, "2024-01-29"),
    (3, 'MCI1040',3, 3, "2024-01-27")
]

try:
    cursor.executemany('''
                INSERT INTO appdocs_manifiesto (id, numero, vehiculo_id, documento_id, fecha_emision)
                VALUES (?, ?, ?, ?, ?) ''', manifiestos_data) 
except:
    print (format_exc())
    print ("Datos Manifiestos ya existen")
 

# Commit the changes and close the connection
conn.commit()
conn.close()

