import requests
from bs4 import BeautifulSoup


def get_response():
    url = 'https://dictionary.cambridge.org/'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    try:
        return requests.get(url, headers=user_agent)
    except requests.exceptions.RequestException:
        return False


def get_data():
    if not get_response():
        return False
    soup = BeautifulSoup(get_response().text, 'lxml')

    print(soup)


if __name__ == '__main__':
    get_data()