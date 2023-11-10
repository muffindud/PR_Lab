# ./
# link_parser.py
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
        body=dumps(data).encode()
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

    channel.queue_declare(queue='999', durable=True)

    print(f" [*] Waiting for messages on thread {thread}.")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()} on thread {thread}.")
        response = get_tags(body.decode())
        name = body.decode().split('/')[-1]
        write_data({
            "name": name,
            "tags": response
        })
        print(f" [x] Done on thread {thread} with {body.decode()}.")

    channel.basic_consume(
        queue='999',
        on_message_callback=callback,
        auto_ack=True
    )

    channel.basic_qos(prefetch_count=1)
    channel.start_consuming()


def main(worker_threads: int = instance_no):
    for i in range(worker_threads):
        threading.Thread(target=consume, args=str(i)).start()


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            print(f"Using {sys.argv[1]} thread(s).")
            main(int(sys.argv[1]))
        else:
            print(f"No arguments provided, using {instance_no} thread(s).")
            main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
