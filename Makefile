.PHONY: run clean requirements env config install pylint jslint lint shell db deploy git

root_path="/opt/eyebrowse"
env_path="$(root_path)/env"
debug_path="$(root_path)/debug"

ifndef env
	env=dev
endif

ifndef debug
	debug=true
endif

shell:
	python manage.py shell

run:
	python manage.py runserver

clean:
	find . -type f -name '*.py[cod]' -delete
	find . -type f -name '*.*~' -delete

requirements:
	pip install -r requirements.txt

git:
	git submodule update --init --recursive

env:
	sudo mkdir -p $(root_path)
	echo $(env) | sudo tee $(env_path) > /dev/null
	echo $(debug) | sudo tee $(debug_path) > /dev/null

config:
	mv config.py config.py-bak 2>/dev/null # save a copy just in case
	cp config_template.py config.py
	git checkout config_template.py # reset the template

db:
	python manage.py syncdb
	python manage.py migrate

install: clean git requirements env config db

pylint:
	-flake8 .

jslint:
	-jshint -c .jshintrc --exclude-path .jshintignore .

lint: clean pylint jslint

deploy: lint
	fab -i prod deploy restart_apache
