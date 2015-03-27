.PHONY: cassandra-install kronos-install metis-install jia-install install cassandra-run kronos-run metis-run jia-run run installdeps

PUBLIC_PORT=80
PWD=$(shell pwd)
KRONOS_ROOT=$(PWD)/kronos
METIS_ROOT=$(PWD)/metis
JIA_ROOT=$(PWD)/jia
# TODO(joshblum): use latest tags
KRONOS_VERSION = "v0.7.2"
METIS_VERSION = "v0.7.1"
JIA_VERSION = "v0.7.1"

default: install

install: installdeps cassandra-install kronos-install metis-install jia-install

installdeps:
	# https://docs.docker.com/installation/ubuntulinux/#installing-docker-on-ubuntu
	wget -qO- https://get.docker.com/ | sh

	# https://www.digitalocean.com/community/tutorials/how-to-install-java-on-ubuntu-with-apt-get
	sudo apt-get install python-software-properties
	sudo add-apt-repository ppa:webupd8team/java
	sudo apt-get update
	sudo apt-get install oracle-java8-installer

run: cassandra-run kronos-run metis-run jia-run

# https://github.com/tobert/cassandra-docker
cassandra-install:
	sudo docker pull tobert/cassandra
	sudo mkdir -p /srv/cassandra

cassandra-run:
	sudo docker run -d -v /srv/cassandra:/data tobert/cassandra

kronos-install:
	mkdir -p $(KRONOS_ROOT)/logs

kronos-run:
	sudo docker run -d -v $(KRONOS_ROOT):/etc/kronos -v $(KRONOS_ROOT)/logs:/var/log/kronos -p 8150:8150 chronology/kronos:$(KRONOS_VERSION)

metis-install:
	mkdir -p $(METIS_ROOT)/logs

metis-run:
	sudo docker run -d -v $(METIS_ROOT):/etc/metis -v $(METIS_ROOT)/logs:/var/log/metis/ -p 8151:8151 chronology/metis:$(METIS_VERSION)

jia-install:
	mkdir -p $(JIA_ROOT)/logs

jia-run:
	sudo docker run -d -v $(JIA_ROOT):/etc/jia -v $(JIA_ROOT)/logs:/var/log/jia/ -p $(PUBLIC_PORT):80 chronology/jia:$(JIA_VERSION)
