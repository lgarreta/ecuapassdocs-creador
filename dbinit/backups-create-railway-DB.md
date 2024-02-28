## Create a new DB service on railway

## Login to Railway and link to project using railway CLI:
railway login
railway link

## Get Railway vars:
railway variables --json > dbvars-railway-db-lgarreta.json

## Source variables:
source-dbvars.py dbvars-railway-db-lgarreta.json > varsPG.sh
source varsPG.sh

## Create DB, USER, and GRANT PRIVILEGES
psql -c "CREATE USER admindb WITH PASSWORD 'admindb';"
psql -c "CREATE DATABASE ecuapassdocsdb WITH OWNER='admindb';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE ecuapassdocsdb TO admindb;"

## Update Railway PG variables to current DB settings:
	PGDATABASE="ecuapassdocsdb"
	PGUSER="admindb"
	PGPASSWORD="admindb2024A."

## Set web DB vars: Set shared variables to the PG variables:
	PGDATABASE="ecuapassdocsdb"
	PGUSER="admindb"
	PGPASSWORD="admindb2024A."
	PGHOST=viaduct.proxy.rlwy.net
	PGPORT=52171

- Copy PG variables to django web app settings
	PGDATABASE="ecuapassdocsdb"
	PGUSER="admindb"
	PGPASSWORD="admindb2024A."
	PGHOST=viaduct.proxy.rlwy.net
	PGPORT=52171

- Create django superuser 'admin'
