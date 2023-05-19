# Mailing

**Mailing** is a project that allows to arrange asynchronous sent-outs of SMS messages to multiple clients, given, if necessary, certain tags and mobile operators.
After every sent-out is organized, messages related to the sent-out are saved with according status. In addition, you can track stats of mailings.

If a mass mailing is to be in some future date, the application executes the command at the set time time.

## Installation

Before pulling from the repository, make sure you have [Docker](https://docs.docker.com/engine/install/) installed.

To clone the project from the repository, on command line, navigate to directory where you would like to store the project and run:

```bass
git clone https://gitlab.com/praktikant101/mailing.git
```

## Set up

Once cloned, in the root directory of the project, where files like "docker-compose", "Dockerfile" are located, create a .env file as per .env_example and fill in environment parameters.

You can set 'DB_ENGINE="django.db.backends.postgresql_psycopg2"' and make sure you to insert TOKEN that will be in mailing via [API](https://probe.fbrq.cloud/docs).

If you want to receive daily messages with stats on mailings executed in the last 24 hours,
you can set the EMAIL parameter in tge .env file. 

To build the project, in the root directory of the application, run:

```bash
docker-compose up --build
```

## Tests

To run tests, you will need id of the relevant container. In a new terminal window, run: 

```bash
docker ps -a
```

Copy the CONTAINER_ID corresponding to **fr-web** under CONTAINER_NAME and paste the copied id of the container and paste it instead of <container_name>:

```bash
docker exec -it <container_id> bash
python manage.py test
```
If you are asked between destroying existing test database, print "yes" and proceed further.

Testing for the **Mailing** model triggers the .create() method of the relevant serializer that initiates sent-out of messages. Thus, by this test we at the same time ensure testing for messages' creation, SMS sent-outs and recording statistics. 


## Optional

You will get a list of docker containers. Select the CONTAINER_ID corresponding to **fr-web** under CONTAINER_NAME and run the following commands:

```bash
docker exec -it <container_id> bash
python manage.py fill_db
```

Once initial data is set up, you can check views. 


## Usage

SMS messages are (asynchronously) sent as soon as a new mailing is created. Clients with same operator code and/or tags,mentioned in the mailing,
are selected as receivers. If you don't mention any additional parameters other than the text body and launch date ("created_at" field),
all clients obtain SMS messages. To see the mailings that have been sent out/relevant stats/messages/clients, you see in http://0.0.0.0:8000. 

