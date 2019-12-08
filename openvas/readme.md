# OpenVas
-------

A Docker container for OpenVAS on Ubuntu.  By default, the latest images includes the OpenVAS Base as well as the NVTs and Certs required to run OpenVAS.  We made the decision to move to 9 as the default branch since 8 seems to have [many issues](https://github.com/mikesplain/openvas-docker/issues/84) in docker.  We suggest you use 9 as it is much more stable. Our Openvas9 build was designed to be a smaller image with fewer extras built in. Please note, OpenVAS 8 is no longer being built as OpenVAS 9 is now standard.  The image is can still be pulled from the Docker hub, however the source has been removed in this github as is standard with deprecated Docker Images.


| Openvas Version | Tag     | Web UI Port |
|-----------------|---------|-------------|
| 9               | latest/9| 443        |


[Dockerfile Details](https://hub.docker.com/r/mikesplain/openvas/dockerfile)
[Details](https://hub.docker.com/r/mikesplain/openvas)


## Setup

Plain setup:

```sh
docker run -d -p 9443:443 --name openvas mikesplain/openvas
```

This will grab the container from the docker registry and start it up. __Openvas startup can take some time (4-5 minutes while NVT's are scanned and databases rebuilt)__, so __be patient__. Once you see a It seems like your OpenVAS-9 installation is OK. process in the logs, the web ui is good to go. Goto `https://localhost:9443`.

```yml
Username: admin
Password: admin
```

To check the status of the process, run:

```sh
docker top openvas
```

In the output, look for the process scanning cert data.  It contains a percentage. We can see the logs, and wait until all is started:

```sh
docker logs openvas
```

To run bash inside the container run:

```sh
docker exec -it openvas bash
```

## Update NVTs
Occasionally you'll need to update NVTs. We update the container about once a week but you can update your container by execing into the container and running a few commands:

```sh
docker exec -it openvas bash
```

Inside the container:

```sh
greenbone-nvt-sync
openvasmd --rebuild --progress
greenbone-certdata-sync
greenbone-scapdata-sync
openvasmd --update --verbose --progress

/etc/init.d/openvas-manager restart
/etc/init.d/openvas-scanner restart
```

The folder `/var/lib/openvas/mgr/` is updated.

## Create a new Image

Once we have updated the NVTs, we can commit the changes and create a new image. First we update the image with the latest patches.

```sh
apt-get update

apt-get upgrade

apt-get autoremove
```