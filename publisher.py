import time
import json

import pika


class Publisher:
    def __init__(self, config):
        self.config = config

    def publish(self, routing_key, message):
        connection = self.create_connection()
        # Create a new channel with the next available channel number
        # or pass in a channel number to use
        channel = connection.channel()
        # Creates an exchange if it does not already exist, and if
        # the exchange exists,
        # verifies that it is of the correct and expected class.
        channel.exchange_declare(
            exchange=self.config['exchange'],
            exchange_type='topic',
        )
        # Publishes message to the exchange with the given routing key
        channel.basic_publish(
            exchange=self.config['exchange'],
            routing_key=routing_key, body=message)
        print(f"[x] Sent message '{message}' for {routing_key}")

    def create_connection(self):
        param = pika.ConnectionParameters(
            host=self.config['host'],
            port=self.config['port'],
        )

        return pika.BlockingConnection(param)


def publish():
    config = {'host': 'localhost', 'port': 5672, 'exchange': 'my_exchange'}
    publisher = Publisher(config)

    while True:
        message = json.dumps({'disaster_happened': False})
        publisher.publish('disaster.alert', message)

        time.sleep(10)


if __name__ == '__main__':
    publish()
