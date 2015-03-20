.PHONY: cassandra-install kronos-install metis-install jia-install install cassandra-run kronos-run metis-run jia-run run

# TODO(joshblum): use latest tags
KRONOS_VERSION = "v0.7.2"
METIS_VERSION = "v0.7.1"
JIA_VERSION = "v0.7.1"

default: install

install: cassandra-install kronos-install metis-install jia-install

run: cassandra-run kronos-run metis-run jia-run

# https://github.com/tobert/cassandra-docker
cassandra-install:
	sudo docker pull tobert/cassandra
	sudo mkdir -p /srv/cassandra

cassandra-run:
	sudo docker run -d -v /srv/cassandra:/data tobert/cassandra

kronos-install:
	sudo mkdir -p /etc/kronos
	sudo cp kronos_settings.py /etc/kronos/settings.py
	sudo mkdir -p /var/log/kronos

kronos-run:
	sudo docker run -d -p 8150:8150 -v /etc/kronos:/etc/kronos -v /var/log/kronos:/var/log/kronos chronology/kronos:$(KRONOS_VERSION)

metis-install:
	sudo mkdir -p /etc/metis
	sudo cp metis_settings.py /etc/metis/settings.py
	sudo mkdir -p /var/log/metis

metis-run:
	sudo docker run -d -v /etc/metis:/etc/metis -v /var/log/metis/:/var/log/metis/ -p 80 chronology/metis:$(METIS_VERSION)

jia-install:
	sudo mkdir -p /etc/jia
	sudo cp jia_settings.py /etc/jia/settings.py
	sudo mkdir -p /var/log/jia

jia-run:
	sudo docker run -d -v /etc/jia:/etc/jia -v /var/log/jia/:/var/log/jia/ -p 80 chronology/jia:$(JIA_VERSION)
