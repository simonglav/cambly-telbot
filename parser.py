import requests
from bs4 import BeautifulSoup


def get_response(url):
    """
    Send a GET request, and if URL is valid - return result, else - False
    :param url: valid URL
    :return: :class:`Response` object or False
    """
    user_agent = {'User-agent': 'Mozilla/5.0'}
    try:
        return requests.get(url, headers=user_agent)
    except requests.exceptions.RequestException:
        return False


def adjust_word(word: str) -> str:
    """
    Transform given word to the required form
    :param word: word to validate
    :return: validated word
    """
    word = word.strip()
    # The longest word in English consists of 45 characters(according to Wiki)
    word = word[:50]
    # Dictionary can contain phrases
    word = word.replace(' ', '-')
    word = word.lower()
    return word


def get_data(word: str) -> dict:
    url = 'https://dictionary.cambridge.org/dictionary/english/' + adjust_word(word)
    if not get_response(url):
        return {}
    soup = BeautifulSoup(get_response(url).text, 'lxml')
    print(soup.find('img', class_='i-amphtml-fill-content i-amphtml-replaced-content'))
    result_dict = {}
    return result_dict


if __name__ == '__main__':
    get_data('apple')
