REST API for send, recieve, update and delete messages
===
## Table of Contents

[TOC]

## Introduction

This API is based on default django application, created by `django-admin`.  It uses just one model, which contain information about sender, reciever and message itself. Format of input data is JSON.
PATCH

## To run
First, you need to create and run containers with `docker-compose up`. Then, migrations should be performed with `docker exec -it django bash migrate.sh`. I decided to move migrations to a separate command, because AFAIK there can be some drawbacks of migration on server startup, especially if application is sharded on several containers. 

## API details

Here you can see my message model:
```python

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.UUIDField(null=False)
    sender_name = models.TextField(max_length=100, default="")
    reciever_id = models.UUIDField(null=False)
    reciever_name = models.TextField(max_length=100, default="")
    text = models.TextField(max_length=1024, editable=True, null=False)
    date = models.DateTimeField(default=timezone.now)

```

Here, `id` is used as primary key, so it should be provided for update and delete message. `sender_id` should be provided for this operations as well. When reading, you need to provide either `sender_id` (in this case all fields are provided), or `reciever_id` (in this case `sender_id` is hidden, but name is still avalible). This is done for security: If reciever can get sender's UUID it can then modify or delete message, but by design it is prohibited. If any extra parameters provided, they are ignored. If required parameters are missed or some parameters are not valid, you will get `Http400` error. If they are valid, but nothing is found, `Http404` error is returned. Post method returns 201 code on success, all other  - 200. 

Here are HTTP methods table (**bold** parameters are required):

|Operation|Method|Parameters|
|-|-|-|
|Read|GET|id, **sender_id** or **reciever_id** (at least one should be provided)|
|Create|POST|**sender_id**, **reciever_id**, **text**,sender_name, reciever_name, date|
|Update|PATCH|**id**, **sender_id**, **text**|
|Delete|DELETE|**id**, **sender_id**|

## Query examples

Some HTTP utility should be used, for example cURL or httpie. Here I will use cURL. 
### Create
For example, observe this request:
```bash
    curl -X POST -d '{"sender_id": "7dc922c8-7cc9-11ea-bb59-ffbc3f2ce715", "reciever_id": "7cc86cda-7cc9-11ea-8133-cfb4280c5b94", "text":"test message"}' http://localhost/api/message/    
```
It will create message with the following content:
```json
{
    "id": "3cc50e3e-2f61-4258-a43f-a941f9db643a", 
    "sender_id": "7dc922c8-7cc9-11ea-bb59-ffbc3f2ce715", 
    "sender_name": "sender", 
    "reciever_id": "7cc86cda-7cc9-11ea-8133-cfb4280c5b94",
    "reciever_name": "reciever",
    "text": "test message", 
    "date": "2020-04-12T09:37:25.492509"
}
```
### Read

If we repeat query, new instance of message will be created, with other time and id. 

Now, let's see on example of getting message:
```bash
    curl -X GET -d '{"sender_id": "7dc922c8-7cc9-11ea-bb59-ffbc3f2ce715"}' http://localhost/api/message/    
```
This query will return us list of messages sent by the user in the following format:
```json
[{
    "id": "3cc50e3e-2f61-4258-a43f-a941f9db643a",
    "sender_id": "7dc922c8-7cc9-11ea-bb59-ffbc3f2ce715",
    "sender_name": "sender",
    "reciever_id": "7cc86cda-7cc9-11ea-8133-cfb4280c5b94", 
    "reciever_name": "reciever",
    "text": "test message",
    "date": "2020-04-12T09:37:25.492509"
}]
```

However, if we get recieved messages with the following query, no sender_id is provided:

```bash
 curl -X GET -d '{"reciever_id": "7cc86cda-7cc9-11ea-8133-cfb4280c5b94"}' http://localhost/api/message/
```

Output:
```json
[{
"id": "3cc50e3e-2f61-4258-a43f-a941f9db643a", 
"sender_name": "sender",
"reciever_id": "7cc86cda-7cc9-11ea-8133-cfb4280c5b94", 
"reciever_name": "reciever", 
"text": "test message",
"date": "2020-04-12T09:50:50.357664"}]
```

### Update

For updating, you have to provide message UUID, sender UUID and new text. 

Example:
```bash
curl -X PATCH -d '{ "id": "3cc50e3e-2f61-4258-a43f-a941f9db643a", "sender_id": "7dc922c8-7cc9-11ea-bb59-ffbc3f2ce715", "text": "new text"}' http://localhost/api/message/
```

This will return updated message:
```json 
{
    "id": "3cc50e3e-2f61-4258-a43f-a941f9db643a", 
    "sender_id": "7dc922c8-7cc9-11ea-bb59-ffbc3f2ce715", 
    "sender_name": "sender", 
    "reciever_id": "7cc86cda-7cc9-11ea-8133-cfb4280c5b94",
    "reciever_name": "reciever",
    "text": "new text", 
    "date": "2020-04-12T09:37:25.492509"
}

```

### Delete

Delete is similar to update in terms of query, but no new text is needed:

```bash
curl -X DELETE -d '{ "id": "3cc50e3e-2f61-4258-a43f-a941f9db643a", "sender_id": "7dc922c8-7cc9-11ea-bb59-ffbc3f2ce715"}' http://localhost/api/message/
```
Output is the same as in update. 