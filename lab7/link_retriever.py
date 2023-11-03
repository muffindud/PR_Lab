# ./
# link_retriever.py
import requests
import bs4 as bs


absolute_home_link = "https://999.md"
relative_link = "/ro/list/real-estate/apartments-and-rooms?o_30_241=894&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776&page="
max_pages = 3


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
