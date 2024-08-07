import pika
import threading
import json
import os
from time import sleep

RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RMQ_USER_PASSW = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")

def consumer(consumer_id):
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_USER_PASSW)
    connection_parameters = pika.ConnectionParameters('rabbitmqserver', credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello', durable=True)

    channel.basic_qos(prefetch_count=1)
    def callback(ch, method, properties, body):
        try:
            print(" Callback%s [x] Received %r" % (consumer_id, body))
            data = body.decode()
            # dict_data = json.loads(data)
            sleep(consumer_id)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Consumer {consumer_id} encountered an error: {e}")
        finally:
            ch.close()
    
    channel.basic_consume(queue='hello', on_message_callback=callback, consumer_tag=f'consumer_{consumer_id}', auto_ack=False)
    channel.start_consuming()

if __name__=="__main__":
    threads = {}
    for i in range(1,4):
        thread = threading.Thread(target=consumer, args=(i,))
        threads[i] = thread
        thread.start()
    print(' [*] Waiting for messages. To exit press CTRL+C')

    while True:
        for i, each in threads.items():
            if not each.is_alive():
                new_thread = threading.Thread(target=consumer, args=(i,))
                new_thread.start()
                threads[i] = new_thread
        sleep(5)
