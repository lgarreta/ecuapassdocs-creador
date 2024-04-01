
## Create postgress DB user and DB using psql commands from linux shell
DBUSER=admindb2
PASSWORD=admindb2
DBNAME=ecuapassdocsdb2

sudo -u postgres createuser $DBUSER
sudo -u postgres psql -c "ALTER USER $DBUSER WITH PASSWORD '$PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE $DBNAME;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $DBUSER";


