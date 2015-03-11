.PHONY: run clean requirements env config install lint

root_path="/opt/eyebrowse"
env_path="$(ROOT_PATH)/env"
debug_path="$(ROOT_PATH)/debug"

ifndef env
	env=dev
endif

ifndef debug
	debug=true
endif

run:
	python manage.py runserver.py

clean:
	find . -type f -name '*.py[cod]' -delete
	find . -type f -name '*.*~' -delete

requirements:
	pip install -r requirements.txt

env:
	sudo mkdir -p $(root_path)
	echo $(env) | sudo tee $(env_path) > /dev/null
	echo $(debug) | sudo tee $(debug_path) > /dev/null

config:
	mv config.py config.py-bak # save a copy just in case
	cp config_template.py config.py

install: clean requirements env config

lint: clean
	# TODO (joshblum): Add jshint stuff
	flake8 .
