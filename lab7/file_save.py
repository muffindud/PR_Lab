# ./
# file_save.py
from json import loads, dumps, decoder
from time import sleep

import pika
import sys
import os
import threading


product_queue = {}
file_write_delay = 10


def write_to_file(key: str, prod: dict):
    try:
        products_file = open("products/products.json", "r")
        file_content = products_file.read()

        if file_content == "":
            file_content = "{}"

        products_file.close()
    except:
        file_content = "{}"

    file_content = loads(file_content)

    products_file = open("products/products.json", "w")

    if key not in file_content.keys():
        file_content[key] = prod

    product_queue.pop(key)

    products_file.write(dumps(file_content, indent=4))

    products_file.close()


def write_to_file_thread():
    while True:
        print("Writing to file")
        temp_product_queue = product_queue.copy()
        for key in temp_product_queue.keys():
            write_to_file(key, temp_product_queue[key])
        temp_product_queue.clear()
        sleep(file_write_delay)


def write_to_queue(content: dict):
    product_queue[content["name"]] = content["tags"]


def consume():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    channel.queue_declare(queue='file_save')

    def callback(ch, method, properties, body):
        data = loads(body.decode())
        print(" [x] Received " + data["name"])
        write_to_queue(data)

    channel.basic_consume(
        queue="file_save",
        on_message_callback=callback,
        auto_ack=True
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def main():
    threading.Thread(target=write_to_file_thread).start()
    threading.Thread(target=consume).start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
