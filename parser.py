import requests
from bs4 import BeautifulSoup
# CED - Cambridge English Dictionary


class Parser:
    def __init__(self, word: str):
        self._word = Parser.adjust_word(word)
        # CED URL + validated word
        self._url = 'https://dictionary.cambridge.org/dictionary/english/' + self._word
        self._description_dictionary = {}

    @staticmethod
    def adjust_word(word: str):
        """
        Transforms the word to a slug form, cut to 49 char
        """
        word = word.strip()
        # The longest word in English consists of 45 characters(according to Wiki)
        word = word[:50]
        # English dictionary can contain phrases
        word = word.replace(' ', '-')
        word = word.lower()
        return word

    def _get_page(self):
        """
        Sends a GET request, and if the URL is valid returns a page, else - False
        """
        user_agent = {'User-agent': 'Mozilla/5.0'}
        try:
            response = requests.get(self._url, headers=user_agent)
            # If CED doesn't possess the word, it redirects to a Home page, i.e. the URL changes
            if response.url == self._url:
                return response.text
        except requests.exceptions.RequestException:
            return False
        else:
            return False

    def get_description(self):

        page = self._get_page()
        # If something goes wrong with request or the word doesn't exist in CED
        if not page:
            return {}

        page_soup = BeautifulSoup(page, 'lxml')
        prime_block = page_soup.find('div', class_='entry-body')
        if not prime_block:
            return {}
        # Decrease the range of BS4 search via chunking the page to smaller blocks
        img_def_block = prime_block.find('div', class_='hflxrev hdf-xs hdb-s hdf-l')
        morphology_pronunciation_block = prime_block.find('div', class_='pos-header dpos-h')
        examples_block = prime_block.find('div', class_='daccord')

        image = None
        definition = None
        # If block is still available and class name wasn't changed
        if img_def_block:
            # Only 'src' of the image is needed
            image = img_def_block.find('amp-img', class_='dimg_i').get("src")
            definition = img_def_block.find('div', class_='def ddef_d db')
            # There's no need in extra spaces and colons at the end
            definition = definition.text.strip()[:-1]

        self._description_dictionary = {
            'definition': definition,
            'image': image,
        }
        return self._description_dictionary


if __name__ == '__main__':
    print(Parser('apple').get_description())
