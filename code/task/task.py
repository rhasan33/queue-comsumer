import os
from time import sleep
from celery import Celery, bootsteps
from kombu import Consumer, Exchange, Queue
import logging

logger = logging.getLogger(__name__)

exchange = Exchange('pathao-food', type='direct')
order_queue = Queue(name='order-queue', exchange=exchange, routing_key='order-queue')
restaurant_queue = Queue(name='restaurant-queue', exchange=exchange, routing_key='restaurant-queue')

celery_app = Celery(
    'consumer',
    broker=os.environ.get('CELERY_BROKER_URL'),
    backend=os.environ.get('CELERY_BROKER_URL')
)


class OrderConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[order_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    def handle_message(self, body, message):
        sleep(15)
        print(body)
        message.ack()


class RestaurantConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[restaurant_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    def handle_message(self, body, message):
        sleep(10)
        print(body)
        message.ack()

celery_app.steps['consumer'].add(OrderConsumer)
celery_app.steps['consumer'].add(RestaurantConsumer)


if __name__ == '__main__':
    celery_app.start()
