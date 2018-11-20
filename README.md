## DDASH
This service deploys docker container running ddash.

##### NB: Make sure diam service is running before performing any steps below. Follow the instructions in diam repository.

#### Setup dev environment
1. Make sure docker is installed and run commands below:

```sh
docker run -p 127.0.0.1:11211:11211 --name memcached -d memcached
cd [ddash directory]
tox -e runserver
```

2. If you need to recreate your tox virtual environment e.g. because of conflicting dependencies, run command below:

```sh
tox --recreate -e runserver
```

#### Build Steps
1. Make sure docker is installed on your system.

2. Run the commands below:

```sh
cd [ddash directory]
docker build -t ddash:latest .
docker run --network docker-net --name memcached -d memcached
docker run -p 8000:80 --network docker-net --env-file .env --name ddash.test ddash:latest
```
Docker run command uses docker-net defined in diam.

3. Go to http://127.0.0.1:8000