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
    links = [
        'https://999.md/ro/81848949',
        'https://999.md/ro/83855434',
        'https://999.md/ro/84029867',
        'https://999.md/ro/84029779',
        'https://999.md/ro/81537475'
    ]

    results = {}

    for link in links:
        results[link] = get_tags(link)

    print(dumps(results, indent=4))


if __name__ == '__main__':
    main()
