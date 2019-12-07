# OpenVas
-------

A Docker container for OpenVAS on Ubuntu.  By default, the latest images includes the OpenVAS Base as well as the NVTs and Certs required to run OpenVAS.  We made the decision to move to 9 as the default branch since 8 seems to have [many issues](https://github.com/mikesplain/openvas-docker/issues/84) in docker.  We suggest you use 9 as it is much more stable. Our Openvas9 build was designed to be a smaller image with fewer extras built in. Please note, OpenVAS 8 is no longer being built as OpenVAS 9 is now standard.  The image is can still be pulled from the Docker hub, however the source has been removed in this github as is standard with deprecated Docker Images.


| Openvas Version | Tag     | Web UI Port |
|-----------------|---------|-------------|
| 9               | latest/9| 443        |

## Setup

Run:

```sh
docker run -d -p 444:443 --name openvas mikesplain/openvas
```

This will grab the container from the docker registry and start it up. __Openvas startup can take some time (4-5 minutes while NVT's are scanned and databases rebuilt)__, so __be patient__. Once you see a It seems like your OpenVAS-9 installation is OK. process in the logs, the web ui is good to go. Goto `https://localhost:444`.

```yml
Username: admin
Password: admin
```

To check the status of the process, run:

```sh
docker top openvas
```

In the output, look for the process scanning cert data.  It contains a percentage.

To run bash inside the container run:

```sh
docker exec -it openvas bash
```

### OpenVAS Manager

To use OpenVAS Manager, add port `9390` to you docker run command:

```sh
docker run -d -p 444:443 -p 9390:9390 --name openvas mikesplain/openvas
```

### Volume Support

We now support volumes. Simply mount your data directory to `/var/lib/openvas/mgr/`:

```sh
mkdir data
cd data
mkdir openvas

docker run -d -p 443:443 -v ./data/openvas:/var/lib/openvas/mgr/ --name openvas mikesplain/openvas
```
Note, __your local directory must exist prior to running__.

#### Set Admin Password

The admin password can be changed by specifying a password at runtime using the env variable `OV_PASSWORD`:

```sh
docker run -d -p 444:443 -e OV_PASSWORD=securepassword41 --name openvas mikesplain/openvas
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

The folder `/var/lib/openvas/mgr/` is updated. We can create a __volume__ to host the data in the host machine - see previous section.

## Docker compose (experimental)

For simplicity a docker-compose.yml file is provided, as well as configuration for Nginx as a reverse proxy, with the following features:

* Nginx as a reverse proxy
* Redirect from port 80 (http) to port 433 (https)
* Automatic SSL certificates from [Let's Encrypt](https://letsencrypt.org/)
* A cron that updates daily the NVTs

We are including in the docker-compose:

* The management port
* A volume. We need to have the directory `data/openvas` created previously

To run:

* Change "www.gz.com" in the following files:
  * [docker-compose.yml](docker-compose.yml)
  * [conf/nginx.conf](conf/nginx.conf)
  * [conf/nginx_ssl.conf](conf/nginx_ssl.conf)
* Change the "OV_PASSWORD" enviromental variable in [docker-compose.yml](docker-compose.yml)
* Install the latest [docker-compose](https://docs.docker.com/compose/install/)
* run `docker-compose up -d`

## Other configurations

### Specify DNS Hostname

By default, the system only allows connections for the hostname "openvas".  To allow access using a custom DNS name, you must use this command:

```sh
docker run -d -p 443:443 -e PUBLIC_HOSTNAME=myopenvas.example.org --name openvas mikesplain/openvas
```

### LDAP Support (experimental)

Openvas do not support full ldap integration but only per-user authentication. A workaround is in place here by syncing ldap admin user(defined by `LDAP_ADMIN_FILTER `) with openvas admin users everytime the app start up.  To use this, just need to specify the required ldap env variables:

```sh
docker run -d -p 443:443 -p 9390:9390 --name openvas -e LDAP_HOST=your.ldap.host -e LDAP_BIND_DN=uid=binduid,dc=company,dc=com -e LDAP_BASE_DN=cn=accounts,dc=company,dc=com -e LDAP_AUTH_DN=uid=%s,cn=users,cn=accounts,dc=company,dc=com -e LDAP_ADMIN_FILTER=memberOf=cn=admins,cn=groups,cn=accounts,dc=company,dc=com -e LDAP_PASSWORD=password -e OV_PASSWORD=admin mikesplain/openvas 
```

### Email Support

To configure the postfix server, provide the following env variables at runtime: `OV_SMTP_HOSTNAME`, `OV_SMTP_PORT`, `OV_SMTP_USERNAME`, `OV_SMTP_KEY`

```sh
docker run -d -p 443:443 -e OV_SMTP_HOSTNAME=smtp.example.com -e OV_SMTP_PORT=587 -e OV_SMTP_USERNAME=username@example.com -e OV_SMTP_KEY=g0bBl3de3Go0k --name openvas mikesplain/openvas
```

