import pika
import json
import os
import sys

RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RMQ_USER_PASSW = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")

if __name__=="__main__":
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_USER_PASSW)
    connection_parameters = pika.ConnectionParameters('rabbitmqserver', credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='direct2_logs', exchange_type='direct')

    routing_key = 'PersonA_house'
    # channel.queue_bind(
    #     exchange='direct_logs', queue="PersonA_house", routing_key=routing_key)
    message = 'Hello World!'
    channel.basic_publish(
        exchange='direct2_logs', routing_key=routing_key, body=message)
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()
    pass
