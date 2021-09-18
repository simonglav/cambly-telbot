import requests
from bs4 import BeautifulSoup


def get_page(url):
    """
    Sends a GET request, and if the URL is valid returns a page, else - False
    :param url: valid URL
    :return: page text or False
    """
    user_agent = {'User-agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=user_agent)
        if response.url == url:
            return response.text
    except requests.exceptions.RequestException:
        return False
    else:
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
    # English dictionary can contain phrases
    word = word.replace(' ', '-')
    word = word.lower()
    return word


def get_data(word: str) -> dict:
    # Dictionary URL + validated word
    url = 'https://dictionary.cambridge.org/dictionary/english/' + adjust_word(word)
    # If something goes wrong with request/the word doesn't exist in eng. dict.
    if not get_page(url):
        return {}
    soup = BeautifulSoup(get_page(url), 'lxml')

    # Decrease the range of BS4 search via partitioning the page to smaller blocks
    img_def_block = soup.find('div', class_='hflxrev hdf-xs hdb-s hdf-l')

    # Only 'src' of the image is needed
    image = img_def_block.find('amp-img', class_='dimg_i').get("src")

    definition = img_def_block.find('div', class_='def ddef_d db')
    # There's no need in extra spaces and colons at the end
    definition = definition.text.strip()[:-1]
    # To return needed data as one object
    result_dict = {
        'definition': definition,
        'image': image,

    }
    return result_dict


if __name__ == '__main__':
    print(get_data('appple'))
