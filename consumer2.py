import pika
import os
from time import sleep


RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RMQ_USER_PASSW = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")

def callback(ch, method, properties, body):
    print(" Callback1 [x] Received %r" % body)
    sleep(1)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback2(ch, method, properties, body):
    print(" Callback2 [x] Received %r" % body)
    sleep(3)
    ch.basic_ack(delivery_tag=method.delivery_tag)


credentials = pika.PlainCredentials(RMQ_USER, RMQ_USER_PASSW)
connection_parameters = pika.ConnectionParameters('rabbitmqserver', credentials=credentials)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=False)
channel.basic_consume(queue='hello',
                      on_message_callback=callback2,
                      auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
