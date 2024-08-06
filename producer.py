import pika

connection_parameters = pika.ConnectionParameters('rabbitmqserver')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

def send_message(message):
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=message)
    print(f" [x] Sent {message}")

send_message('Hello, World!')
connection.close()
