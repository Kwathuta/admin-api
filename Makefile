migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

server:
	python manage.py runserver

superuser:
	python manage.py createsuperuser

shell:
	pipenv shell