# ./
# main.py
from src.link_retriever import get_links, absolute_home_link, relative_link
from src.link_processor import send_link


max_links = 5


def main():
    links = get_links(absolute_home_link + relative_link, 1)
    print(links)

    if max_links != 0:
        links = links[0:max_links]

    for link in links:
        send_link(link)


if __name__ == "__main__":
    main()
