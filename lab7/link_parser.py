# ./
# link_parser.py
import json

import pika
import sys
import os
import requests
import bs4 as bs
from json import dumps
import threading

instance_no = 5


def write_data(data: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    channel.queue_declare(queue='file_save')

    channel.basic_publish(
        exchange='',
        routing_key='file_save',
        body=json.dumps(data).encode()
    )


def get_tags(url):
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    keys = []
    values = []
    result = {}

    for key in soup.find_all("span", class_="adPage__content__features__key"):
        keys.append(key.text.strip())

    for value in soup.find_all("span", class_="adPage__content__features__value"):
        values.append(value.text.strip())

    for key in keys:
        result[key] = values[keys.index(key)] if keys.index(key) < len(values) else True

    return result


def consume(thread: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # channel.exchange_declare(exchange='999', exchange_type='fanout')

    # result = channel.queue_declare(queue='', exclusive=True)
    # queue_name = result.method.queue

    # channel.queue_bind(exchange='999', queue=queue_name)

    channel.queue_declare(queue='999', durable=True)

    print(f" [*] Waiting for messages on thread {thread}.")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()} on thread {thread}")
        response = get_tags(body.decode())
        name = body.decode().split('/')[-1]
        write_data({
            "name": name,
            "tags": response
        })

    # channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(
        queue='999',
        on_message_callback=callback,
        auto_ack=True
    )

    channel.basic_qos(prefetch_count=1)
    channel.start_consuming()


def main():
    for i in range(instance_no):
        threading.Thread(target=consume, args=str(i)).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
