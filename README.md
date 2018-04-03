Postgresql server start- sudo service postgresql start

Commands for creating the user, database and setting the user password 

1. sudo -i -u postgres
2. psql
3. CREATE USER admin;
4. ALTER USER admin WITH PASSWORD 'helloworld';
5. CREATE DATABASE alumni_portal OWNER admin;


CREATING SUPER USER-
python manage.py createsuperuser

