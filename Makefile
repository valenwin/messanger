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
