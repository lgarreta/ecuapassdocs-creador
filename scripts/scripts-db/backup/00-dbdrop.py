#!/usr/bin/env python
"""
Remove user and database
"""

DBUSER="admindb2"
DBNAME="ecuapass2"

if input (f"Remove USER: {$DBUSER} and DATABASE: {DBNAME}") == "YES":
	os.system ('sudo -u postgres psql -c "drop user $DBUSER;"')
	os.system ('sudo -u postgres psql -c "drop database $DBNAME;"')


