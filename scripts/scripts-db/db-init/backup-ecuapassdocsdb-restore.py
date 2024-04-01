#!/usr/bin/env python3

"""
Restore backups file from 'pg_dump' into remote_databse
"""
import subprocess, json

#---------------------------------------------------------------------
#---------------------------------------------------------------------
def restore_postgres_database (credentials, input_file):
    command = [
        'pg_restore',
        '-U', credentials ["PGUSER"],
        '-h', credentials ['PGHOST'],
        '-d', credentials ['PGDATABASE'],
		'-p', credentials ['PGPORT'],
        '-c',  # Clean the database before restore
        input_file
    ]
    env = {
        'PGPASSWORD': credentials ["PGPASSWORD"]
    }
    try:
        subprocess.run(command, env=env, check=True)
        print("Database restore completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
#---------------------------------------------------------------------
#---------------------------------------------------------------------

# Usage example
input_credentials = "dbvars-lgarreta.json"
credentials       = json.load (open (input_credentials))
print (credentials)
#
input_file = "backup-ecuapassdocs-railway-db-garretaluis.data"
restore_postgres_database (credentials, input_file)

