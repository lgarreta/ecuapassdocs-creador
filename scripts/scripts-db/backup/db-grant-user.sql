# Connect to the remote postgres database
psql -h $PGHOST -U $PGUSER -p $PGPORT 

# Create database, user, and permissions

CREATE DATABASE dbname;
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;

GRANT CONNECT ON DATABASE ecuapassdocsdb TO byza;


