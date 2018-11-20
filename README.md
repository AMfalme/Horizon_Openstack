## DDASH
This service deploys docker container running ddash.

##### NB: Make sure diam service is running before performing any steps below. Follow the instructions in diam repository.

#### Setup dev environment
1. Setup a python virtualenv for ddash
2. Run commands below:

```sh
cd [ddash directory]
source {ddash_env}/bin/activate
tox -e runserver
```

4. If compress is disabled in local_settings file, make sure to recreate tox env when running the server:

```sh
tox --recreate -e runserver
```

#### Build Steps
1. Make sure docker is installed on your system.

3. Run the commands below:

```sh
cd [ddash directory]
docker build -t ddash:latest .
docker run -p 8000:80 --env-file .env --name ddash.test ddash:latest
```

4. Go to http://127.0.0.1:8000