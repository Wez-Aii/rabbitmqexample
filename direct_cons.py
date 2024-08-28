import pika
import json
import os
import sys

RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RMQ_USER_PASSW = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

if __name__=="__main__":
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_USER_PASSW)
    connection_parameters = pika.ConnectionParameters('rabbitmqserver', credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    # channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # result = channel.queue_declare(queue='PersonA_house', exclusive=True)
    result = channel.queue_declare(queue='PersonA_house', durable=True)
    result = channel.queue_declare(queue='PersonB_house', durable=True)
    result = channel.queue_declare(queue='PersonC_house', durable=True)
    queue_name = result.method.queue
    print(f"queue_name - ({type(queue_name)}) {queue_name}")

    routing_key = "houseA"
    channel.queue_bind(
        exchange='direct_logs', queue='PersonA_house', routing_key=routing_key)
    channel.queue_bind(
        exchange='direct_logs', queue='PersonB_house', routing_key=routing_key)
    channel.queue_bind(
        exchange='direct_logs', queue='PersonC_house', routing_key=routing_key)
    
    channel.queue_bind(exchange='fanout_logs', queue='PersonC_house')

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(
        queue='PersonA_house', on_message_callback=callback, auto_ack=True)

    channel.basic_consume(
        queue='PersonB_house', on_message_callback=callback, auto_ack=True)

    channel.basic_consume(
        queue='PersonC_house', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

    connection.close()