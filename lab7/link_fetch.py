# ./
# link_fetch.py
import pika
import requests
import bs4 as bs
import sys


absolute_home_link = "https://999.md"
relative_link = "/ro/list/real-estate/apartments-and-rooms?o_30_241=894&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776&page="

max_pages = 3
max_links = 5


def get_links(page_link, page, walked_pages=1) -> list:

    # Get page content
    response = requests.get(page_link + str(page))

    # Store links
    links = []

    # Parse page content
    soup = bs.BeautifulSoup(response.text, "html.parser")

    # Find all the ad links
    for link in soup.find_all("a", class_="js-item-ad"):
        l = link.get("href")

        # Check if the link is not already in the list and if it is an ad link
        if l[0:4] == "/ro/" and absolute_home_link + l not in links:
            links.append(absolute_home_link + l)

    # If there are more pages, and we haven't walked enough pages, get the links from the next page
    if links != 0 and (walked_pages < max_pages or max_pages == 0):
        return links + get_links(page_link, page + 1, walked_pages + 1)

    return links


def send_link(link):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # channel.exchange_declare(exchange='999', exchange_type='fanout')
    channel.queue_declare(queue='999', durable=True)

    channel.basic_publish(
        # exchange='999',
        exchange='',
        routing_key='999',
        body=link.encode('utf-8'),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
        )
    )
    print(" [x] Sent '${link}'".format(link=link))

    connection.close()


def main(max_l: int = 0, start_page: int = 1):
    links = get_links(absolute_home_link + relative_link, start_page)

    if max_l != 0:
        links = links[0:max_l]

    for link in links:
        send_link(link)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]), int(sys.argv[2]))
    else:
        print("Usage: link_fetch.py [max_links_to_parse] [starting_page]")
        print("Arg: 0 - no limit")
