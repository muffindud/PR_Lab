# RabbitMQ


## Tasks:

1. Implement the url link extractor as a produce. It should after extracting the products url from the listing page push them to RabbitMQ Queue. (0.5 points)
2. Implement the product details parser functionality as a consumer. It should extract a url from the RabbitMQ queue parse the product details and write this data in a location of persistence. Then take another url from queue and so on. (0.5 points)
3. You should be able to run multiple consumers concurrently. The number of running threats should be settable. (0.5 points)
4. Implement a way of persistence. Either a data base or field. (0.5 points)


## Pre-requisites(first time):

#### Linux:

```bash
python -m venv venv & source venv/bin/activate
```

#### Windows:

```bash
python -m venv venv & venv\Scripts\activate.bat
```


## Implementation:

The project contains 3 modules:
1. __link_fetch.py__: Used for fetching the links from the listing page and pushing them to the queue.

Usage: `python link_fetch.py [max_links_to_parse] [starting_page] <max_pages>`

2. __link_parser.py__: Used for parsing the links from the queue and storing them in the database.

Usage: `python link_parser.py <threads_no>`

3. __file_save.py__: Used for saving the data in a file. It creates a single instance worker to write in a json file.

Usage: `python file_save.py`
