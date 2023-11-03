# ./
# link_parser.py
import pika
import sys
import os
import requests
import bs4 as bs
from json import dumps


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


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='999', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='999', queue=queue_name)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        response = get_tags(body.decode())
        name = body.decode().split('/')[-1]
        f = open(f"products/{name}.json", "w")
        f.write(dumps(response, indent=4))
        f.close()
        print(" [x] Done")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.basic_qos(prefetch_count=1)
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
