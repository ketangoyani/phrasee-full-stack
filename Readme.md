### Phrasee Assignment

## Installation
### Requirements
It's all dockerised, so there are only a couple of requirements to get started:
- [docker](https://docs.docker.com/get-docker/), to run containerised applications
- [docker-compose](https://docs.docker.com/compose/install/), to run multi-container applications

### (Optional - Linux only) Docker post-installation steps

On Linux, there are a couple of [optional post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) that can make it easier to work with Docker. Specifically, the instructions below assume you've set up docker to be manageable as a non-root user. Without this step, you will likely have to run the docker commands with `sudo`.

On older versions of Ubuntu, we've seen DNS issues with the Docker daemon, so it would be prudent to run through the step that set the Docker daemon up to use custom DNS servers.

### (Mac OS/Windows only) Configure resources

On Mac OS and Windows, the default Docker installation is Docker Desktop, which restricts the resources docker can access. This can result in Docker Compose running slowly or run out of memory, so it's a good idea to [increase the available resources docker has access to](https://docs.docker.com/docker-for-mac/#resources), especially memory.


### Setup

The following commands set up a completely fresh copy of the system:
unzip directory and go inside directory
```
docker-compose up
```

## Running

The entire system is dockerized and can be run with `docker-compose up`.
In the local development environment, the system consists of 3 services, which
are defined in the `docker-compose.yml` file.


### Connecting to the local website

Once Docker Compose is up, you should be able to connect to
http://localhost:3000/ and see the Notification home page. 
Postgres will not be accessible directly from the Docker host. 
The node container can be accessed at http://localhost:3000/ and is 
currently only used by the regular front-end

### Intro to docker-compose

Docker Compose starts the services defined in `docker-compose.yml` as docker
containers. Each docker container is similar to a virtual machine and is
independant from the host system. Docker is a vital part of our system and a
key part of many modern production systems. The
[docker documentation](https://docs.docker.com/) is an excellent source to
learn more. There are a couple of key commands that will be useful in your
day-to-day:

- `docker-compose up`: starts all the service containers. If no containers exists, it will build them first.
- `docker-compose build`: rebuild the containers, destroying any previous changes and building new features or dependencies.
- `docker-compose exec <service-name> <command>`: connect to the service container and run a command. Usually, the service name will be `web` or `node` and the command will be `bash`.
- `docker-compose restart <service-name>`: restart a running service. This will be necessary when a service crashed. This is especially common for the `web` service.



