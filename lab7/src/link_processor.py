# ./
# link_processor.py
import pika


def send_link(link):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='999', exchange_type='fanout')

    channel.basic_publish(
        exchange='999',
        routing_key='',
        body=link.encode('utf-8')
    )
    print(" [x] Sent '${link}'".format(link=link))

    connection.close()
