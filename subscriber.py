import sys
import json

import pika


class Subscriber:
    def __init__(self, queue_name, binding_key, config):
        self.queue_name = queue_name
        self.binding_key = binding_key
        self.config = config
        self.connection = self._create_connection()

    def __del__(self):
        self.connection.close()

    def _create_connection(self):
        parameters = pika.ConnectionParameters(
            host=self.config['host'],
            port=self.config['port'],
        )

        return pika.BlockingConnection(parameters)

    def on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key
        message = json.loads(body)
        print(f"[x] Received new message '{message}' for -" + binding_key)

    def setup(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.config['exchange'],
                                 exchange_type='topic')
        # This method creates or checks a queue
        channel.queue_declare(queue=self.queue_name)
        # Binds the queue to the specified exchange
        channel.queue_bind(
            queue=self.queue_name,
            exchange=self.config['exchange'],
            routing_key=self.binding_key,
        )
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_message_callback,
            auto_ack=True,
        )
        print(f'[*] Waiting for data for {self.queue_name}. To exit press CTRL + C')
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


def subscribe():
    config = {'host': 'localhost', 'port': 5672, 'exchange': 'my_exchange'}

    if len(sys.argv) < 2:
        print('Usage: ' + __file__ + ' <queue_name> <binding_key>')
        sys.exit()
    else:
        queue_name = sys.argv[1]
        # key in the form exchange.*
        key = sys.argv[2]
        subscriber = Subscriber(queue_name, key, config)
        subscriber.setup()


if __name__ == '__main__':
    subscribe()
