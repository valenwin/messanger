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
	. venv/bin/activate; python main.py

db: venv/bin/activate ## Run migrations
	. venv/bin/activate; python manage.py migrate

python-flake:
	-flake8 *.py
	-flake8 apps/accounts/*.py
	-flake8 apps/dialogs/*.py
	-flake8 $(PROJECT)/*.py --exclude settings.py

python-mypy:
	-mypy *.py
	-mypy apps/accounts/*.py
	-mypy apps/dialogs/*.py
	-mypy $(PROJECT)/*.py

python-black:
	-black *.py
	-black apps/accounts/*.py
	-black apps/dialogs/*.py
	-black $(PROJECT)/*.py

