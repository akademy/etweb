# stuff I did


## run server
python manage.py runserver


## migrate model changes
python manage.py makemigrations webapp
python manage.py migrate


## database stuff

### export database
python manage.py dumpdata -o wm.database.dummy.json --exclude=auth --exclude=contenttypes

### import database
python manage.py migrate
python manage.py loaddata "path/to/fixture/file"


### initial set up of database
- create database "etd" (via env MARIADB_DATABASE)
- docker-compose exec web /bin/bash
	- python manage.py migrate
	- python manage.py createsuperuser
	- python manage.py loaddata wm.database.initial.json
	
Could instead load some dummy data with wm.database.dummy.json

## indexing

The indexing will not overright information already in the database. It can be run multiple times.
Start by adding all the data from the CSVs. (folder-name could be "data-full")

	python web/manage.py data-import {folder-name}

Then pull in info from wikidata. This will take some time in an effort to reduce the load on wikidata

	python web/manage.py wikidata-updater

And then update the wikipedia info

	python web/manage.py wikipedia-updater

