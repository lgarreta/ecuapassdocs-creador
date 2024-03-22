## Create postgres user
sudo -u postgres createuser admindb
sudo -u postgres psql -c "ALTER USER admindb WITH PASSWORD 'admindb2024A.';"
sudo -u postgres psql -c "CREATE DATABASE ecuapassdocsdb;"
