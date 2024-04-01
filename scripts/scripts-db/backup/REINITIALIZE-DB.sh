
DBUSER=admindb2
DBNAME=ecuapassdocsdb2


##---------- REINITIALIZE DB --------------------------
## Remove all data and reinitialize DB
python manage.py flush --noinput


##---------- REMOVE USER/DB and CREATE again ------
DBUSER=admindb2
PASSWORD=admindb2
DBNAME=ecuapassdocsdb2

## Remove user and database
sudo -u postgres psql -c "drop user $DBUSER;"
sudo -u postgres psql -c "drop database $DBNAME;"

## Create postgress DB user and DB using psql commands from linux shell
sudo -u postgres createuser $DBUSER
sudo -u postgres psql -c "ALTER USER $DBUSER WITH PASSWORD '$PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE $DBNAME;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $DBUSER";

## Remove all data and reinitialize DB
USER=admin
PSWD=admin
EMAIL=$USER@gmail.com

## Remove old migrations and make migrations
rm appdocs/migrations/00*.py
rm appusuarios/migrations/00*.py

## Run migrations and create superuser
python manage.py flush --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput --username $USER --email $EMAIL --password $PSWD


