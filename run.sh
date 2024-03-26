pip install --upgrade ecuapassdocs
python manage.py createsuperuser
python manage.py collectstatic
python manage.py migrate
python manage.py runserver
sudo -u postgres psql

# Database connection
psql -U byza -h monorail.proxy.rlwy.net -p 54626 ecuapassdocsdb
