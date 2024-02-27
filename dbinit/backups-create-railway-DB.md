- Create a new DB service on railway
- Copy Railway DB settings:

	PGHOST=viaduct.proxy.rlwy.net
	PGUSER=postgres
	PGPASSWORD=3GAdAdBCCgAd5E*c4EFc54Eaf-D35a1D
	PGPORT=52171

- Connect to Railway server as a 'postgres' superuser
	linux=$ psql -h $PGHOST -U $PGUSER -p $PGPORT

- Create DB, USER, and GRANT PRIVILEGES
	railway=# CREATE DATABASE ecuapassdocsdb;
	railway=# CREATE USER admindb WITH PASSWORD 'XXX';
	railway=# GRANT ALL PRIVILEGES ON DATABASE ecuapassdocsdb TO admindb;

- Set postgress DB: Set Railway PG variables to previous DB settings:
	PGDATABASE="ecuapassdocsdb"
	PGUSER="admindb"
	PGPASSWORD="admindb2024A."

- Set web DB vars: Set shared variables to the PG variables:
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
