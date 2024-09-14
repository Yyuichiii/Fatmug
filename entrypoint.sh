#!/bin/sh


# Run migrations
python fatmug/manage.py makemigrations
python fatmug/manage.py migrate



# Start the Django development server
exec python fatmug/manage.py runserver 0.0.0.0:8000
