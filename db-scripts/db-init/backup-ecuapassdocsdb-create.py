#!/usr/bin/env python3

import subprocess

def backup_postgres_database(db_name, db_user, db_password, db_host, db_port, output_file):
    command = [
        'pg_dump',
        '-d', db_name,
        '-U', db_user,
        '-h', db_host,
		'-p', db_port,
        '-Fc',# Custom format
        '-f', output_file
    ]
    env = {
        'PGPASSWORD': db_password
    }
    try:
        subprocess.run(command, env=env, check=True)
        print (f"Backup completed successfully. Output file: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Usage example
db_name = "ecuapassdocsdb"
db_user = "admindb"
db_password = "admindb"
db_host = "monorail.proxy.rlwy.net"
db_port = "54626"
output_file = "backup-ecuapassdocs-railway-db-garretaluis.data"

backup_postgres_database(db_name, db_user, db_password, db_host, db_port, output_file)

