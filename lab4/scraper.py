import requests
import bs4 as bs
import re
import json


url = "http://127.0.0.1:8080"


def find_links(response):
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    links = []

    for link in soup.find_all("a"):
        links.append(url + link.get("href")) if url + link.get('href') not in links else None
    print(links)
    return links


def parse_product(response):
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    product = {}

    for tag in soup.find_all('p'):
        if tag.getText()[0:6] == "Name: ":
            product["name"] = tag.getText()[6:]
        elif tag.getText()[0:8] == "Author: ":
            product["author"] = tag.getText()[8:]
        elif tag.getText()[0:7] == "Price: ":
            product["price"] = tag.getText()[7:]
        elif tag.getText()[0:13] == "Description: ":
            product["description"] = tag.getText()[13:]
    print(product)
    return product


def main():
    parsed_links = []
    new_links = [url]

    for link in new_links:
        response = requests.get(link)

        if response.status_code == 200:
            if re.search(r"/product/\d+$", link):
                product = parse_product(response)
                f = open("dumps/{}.json".format(link.replace('/', '-')), "w")
                f.write(json.dumps(product, indent=4))
                f.close()
            else:
                f = open("dumps/{}.html".format(link.replace('/', '-')), "w")
                f.write(response.text)
                f.close()

            page_links = find_links(response)
            for page_link in page_links:
                if page_link not in new_links:
                    new_links.append(page_link)

            parsed_links.append(link)


if __name__ == '__main__':
    main()
