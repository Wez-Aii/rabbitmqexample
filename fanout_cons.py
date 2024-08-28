#!/usr/bin/env python
import pika
import os

RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RMQ_USER_PASSW = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")

def callback(ch, method, properties, body):
    print(f" [x] {body}")

if __name__=="__main__":
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_USER_PASSW)
    connection_parameters = pika.ConnectionParameters('rabbitmqserver', credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    # channel.exchange_declare(exchange='fanout_logs', exchange_type='fanout')

    # result = channel.queue_declare(queue='', exclusive=True)
    # queue_name = result.method.queue
    queue_name = "amq.gen-vEobltZWbamoTE0Ic8zA3Q"
    print(f"queue_name - ({type(queue_name)}) {queue_name}")

    channel.queue_bind(exchange='fanout_logs', queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()