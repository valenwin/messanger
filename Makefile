PROJECT=yalantis-django

.PHONY: all \
		setup \
		run

venv/bin/activate: ## alias for virtual environment
	python -m venv venv

setup: venv/bin/activate ## project setup
	. venv/bin/activate; pip install pip wheel setuptools
	. venv/bin/activate; pip install -r requirements.txt

run: venv/bin/activate ## Run
	. venv/bin/activate; python manage.py runserver

db: venv/bin/activate ## Run migrations
	. venv/bin/activate; python manage.py migrate

python-flake:
	-flake8 *.py --max-line-length 100
	-flake8 apps/accounts/*.py --max-line-length 100
	-flake8 apps/dialogs/*.py --max-line-length 100
	-flake8 $(PROJECT)/*.py --max-line-length 100

python-mypy:
	-mypy *.py --ignore_missing_imports True
	-mypy apps/accounts/*.py --ignore_missing_imports True
	-mypy apps/dialogs/*.py --ignore_missing_imports True
	-mypy $(PROJECT)/*.py --ignore_missing_imports True

python-black:
	-black *.py
	-black apps/accounts/*.py
	-black apps/dialogs/*.py
	-black $(PROJECT)/*.py

