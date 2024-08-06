import pika
import json

def send_message(message):
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode = pika.DeliveryMode.Persistent
                        ))
    print(f" [x] Sent {message}")


if __name__=="__main__":
    connection_parameters = pika.ConnectionParameters('rabbitmqserver')
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
