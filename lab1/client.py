import requests


def main():
    url = 'http://localhost:5000'

    # GET request
    response = requests.get(url + '/yaass')
    print(response.json())

    # POST request
    response = requests.post(url + '/gimme', json={'name': 'John', 'surname': 'Doe', 'age': 42})
    print(response.json())

    # GET request for a POST route
    response = requests.get(url + '/gimme')
    print(response.json())


if __name__ == '__main__':
    main()
