## disaster_tracker

### Run rabbitmq server
`docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

### Start publisher
`python publisher.py`

### Subscribe on disaster publisher
`python subscriber.py events disaster.*`
