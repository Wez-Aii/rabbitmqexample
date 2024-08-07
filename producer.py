import pika
import json
import os

RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RMQ_USER_PASSW = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")

def send_message(message):
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode = pika.DeliveryMode.Persistent
                        ))
    print(f" [x] Sent {message}")


if __name__=="__main__":
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_USER_PASSW)
    connection_parameters = pika.ConnectionParameters('rabbitmqserver', credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello', durable=True)
    for i in range(15):
        _msg = json.dumps({"data": {"payload": {"key_name": i}, "refresh_token": "token"}}).encode()
        # if i % 7:
        #     _msg = json.dumps({"data": {"payload": {"key_name": i}, "refresh_token": "token"}}).encode()
        # else:
        #     _msg = "hello you"
        send_message(_msg)
    connection.close()
    pass
