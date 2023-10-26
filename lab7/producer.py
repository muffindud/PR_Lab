# ./
# producer.py
import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=b'Hello World!',
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
    print(" [x] Sent 'Hello World!'")

    connection.close()


if __name__ == "__main__":
    main()
