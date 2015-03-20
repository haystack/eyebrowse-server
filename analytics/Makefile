.PHONY: cassandra-install kronos-install metis-install jia-install install

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

