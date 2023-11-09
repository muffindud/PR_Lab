# ./
# link_fetch.py
import pika
import requests
import bs4 as bs
import sys


absolute_home_link = "https://999.md"
relative_link = "/ro/list/real-estate/apartments-and-rooms?o_30_241=894&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776&page="


def get_links(page_link, page, max_p, walked_pages=1) -> list:
    response = requests.get(page_link + str(page))

    links = []

    soup = bs.BeautifulSoup(response.text, "html.parser")

    # Find all the ad links
    for link in soup.find_all("a", class_="js-item-ad"):
        l = link.get("href")

        if l[0:4] == "/ro/" and absolute_home_link + l not in links:
            links.append(absolute_home_link + l)

    if links != 0 and (walked_pages < max_p or max_p == 0):
        return links + get_links(page_link, page + 1, max_p, walked_pages + 1)

    return links


def send_link(link):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='999', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='999',
        body=link.encode('utf-8'),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
        )
    )
    print(" [x] Sent '${link}'".format(link=link))

    connection.close()


def main(max_l: int = 0, start_page: int = 1, max_p: int = 5):
    links = get_links(absolute_home_link + relative_link, max_p, start_page)

    if max_l != 0:
        links = links[0:max_l]

    for link in links:
        send_link(link)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        main(int(sys.argv[1]), int(sys.argv[2]), max_pages)
    else:
        print("Usage: link_fetch.py [max_links_to_parse] [starting_page], <max_pages>")
        print("Arg: 0 - no limit")
        print("max_pages default: 5")
