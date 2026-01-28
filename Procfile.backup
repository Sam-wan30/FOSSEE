web: cd backend && gunicorn chemical_equipment.wsgi:application --bind 0.0.0.0:$PORT
release: cd backend && python manage.py migrate
