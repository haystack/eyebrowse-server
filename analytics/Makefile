.PHONY: cassandra-install kronos-install metis-install jia-install install

# TODO(joshblum): use latest tags
KRONOS_VERSION = "v0.7.2"
METIS_VERSION = "v0.7.1"
JIA_VERSION = "v0.7.1"

default: install

install: cassandra-install kronos-install metis-install jia-install

# https://github.com/tobert/cassandra-docker
cassandra-install:
	sudo docker pull tobert/cassandra
	sudo mkdir /srv/cassandra
	sudo docker run -d -v /srv/cassandra:/data tobert/cassandra

kronos-install:
	sudo mkdir -p /etc/kronos
	sudo cp kronos_settings.py /etc/kronos/settings.py
	sudo mkdir -p /var/log/kronos
	sudo docker run -d -p 8150:8150 -v /etc/kronos:/etc/kronos -v /var/log/kronos:/var/log/kronos chronology/kronos:$(KRONOS_VERSION)

metis-install:
	sudo mkdir -p /etc/metis
	sudo cp metis_settings.py /etc/metis/settings.py
	sudo mkdir -p /var/log/metis
	docker run -v /etc/metis:/etc/metis -v /var/log/metis/:/var/log/metis/ -p PUBLIC_PORT:80 chronology/metis:$(METIS_VERSION)

jia-install:
	sudo mkdir -p /etc/jia
	sudo cp jia_settings.py /etc/jia/settings.py
	sudo mkdir -p /var/log/jia
	docker run -v /etc/jia:/etc/jia -v /var/log/jia/:/var/log/jia/ -p PUBLIC_PORT:80 chronology/jia:v0.7.1
