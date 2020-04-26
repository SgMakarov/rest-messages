REST API for send, receive, update and delete messages
===

## Introduction


This API is based on default django application, created by `django-admin`.  It uses just one model, which contain information about sender, receiver and message itself. Format of input data is JSON. I've removed this security stuff
with different message views for sender and receiver, as it is still unsafe 
(consider sender, that can edit any message sent by person he is writing to)


## To run
First, you need to create and run containers with `docker-compose up`. Then, migrations should be performed with `docker exec -it django bash migrate.sh`. I decided to move migrations to a separate command, because AFAIK there can be some drawbacks of migration on server startup, especially if application is sharded on several containers. 

## API details

All details, such as: responce codes, parameters, sample queries and even test enviromnemt is avalible at http://localhost/api/swagger/. Be aware, that due to some django properties you will need to serve staticsby yourself, if DEBUG is set to false, (with simple command to `manage.py`, but still), and statics are needed for `swagger.ui`. 


Here are API methods: ![Image](https://i.imgur.com/qG0iOuA.png) 
