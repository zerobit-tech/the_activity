#!/bin/bash

find . -name "*.pyc" -exec rm {} \;
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

rm db.sqlite3

python manage.py migrate
python manage.py loaddata the_activity
