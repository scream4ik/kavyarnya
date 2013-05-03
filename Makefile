.PHONY: requirements requirements-upgrade freeze syncdb run run-public makemessages compilemessages south collectstatic cloc clean

project_name=kavyarnya

requirements:
	-@echo "### Installing requirements"
	-@pip install -r requirements.txt

requirements-upgrade:
	-@echo "### Upgrading requirements"
	-@pip freeze | cut -d = -f 1 | xargs pip install -U

freeze:
	-@echo "### Freezing python packages to requirements.txt"
	-@pip freeze > requirements.txt

syncdb:
	-@echo "### Creating database tables and loading fixtures"
	@PYTHONPATH=$(PYTHONPATH):. DJANGO_SETTINGS_MODULE=$(project_name).settings python manage.py syncdb --noinput
	@PYTHONPATH=$(PYTHONPATH):. DJANGO_SETTINGS_MODULE=$(project_name).settings python manage.py loaddata fixtures/*

run:
	@PYTHONPATH=$(PYTHONPATH):. DJANGO_SETTINGS_MODULE=$(project_name).settings python manage.py runserver --insecure

run-public:
	@PYTHONPATH=$(PYTHONPATH):. DJANGO_SETTINGS_MODULE=$(project_name).settings python manage.py runserver 0.0.0.0:8000 --insecure

makemessages:
	-@django-admin.py makemessages --all

compilemessages:
	-@django-admin.py compilemessages

# If the first argument is "south"...
ifeq (south,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "south"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
south:
	-@python manage.py schemamigration $(RUN_ARGS) --auto
	-@python manage.py migrate $(RUN_ARGS)

collectstatic:
	@python manage.py collectstatic

cloc:
	-@echo "### Counting lines of code within the project"
	-@echo "# Total:" ; find . -iregex '.*\.py\|.*\.js\|.*\.html\|.*\.css' -type f -exec cat {} + | wc -l
	-@echo "# Python:" ; find . -name '*.py' -type f -exec cat {} + | wc -l
	-@echo "# JavaScript:" ; find . -name '*.js' -type f -exec cat {} + | wc -l
	-@echo "# HTML:" ; find . -name '*.html' -type f -exec cat {} + | wc -l
	-@echo "# CSS:" ; find . -name '*.css' -type f -exec cat {} + | wc -l

clean:
	-@echo "### Cleaning *.pyc files "
	-@find . -name '*.pyc' -exec rm -f {} \;