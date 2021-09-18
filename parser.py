import requests
from bs4 import BeautifulSoup
# CED - Cambridge English Dictionary


class Parser:
    # Cambridge English Dictionary URL
    CED_URL = 'https://dictionary.cambridge.org/dictionary/english/'

    # Decrease the range of BS4 search via chunking the page to smaller blocks
    # Common block to all needed data
    PRIME_DIV_CLASS = 'entry-body'

    # Image and word definition block
    IMG_DEF_DIV_CLASS = 'hflxrev hdf-xs hdb-s hdf-l'
    AMP_IMG_CLASS = 'dimg_i'
    DEF_DIV_CLASS = 'def ddef_d db'

    # Name, morphology and pronunciations block
    NAME_MORPH_PRONOUN_DIV_CLASS = 'pos-header dpos-h'
    NAME_SPAN_CLASS = 'hw dhw'
    MORPH_SPAN_CLASS = 'pos dpos'
    PRONOUN_SPAN_CLASS = 'daud'


    # Examples block
    EXAMPLES_LI_CLASS = 'eg dexamp hax'

    def __init__(self, word: str):
        self._word = Parser.adjust_word(word)
        self._url = Parser.CED_URL + self._word
        self._prime_block = ''
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

    def get_description(self) -> dict:
        """
        Returns a word description in dictionary format with keys:
        'name', 'image', 'definition', 'morphology', 'pronunciations'{'UK':,'US':}, 'examples'[]
        """
        page = self._get_page()
        # If something goes wrong with request or the word doesn't exist in CED
        if not page:
            return {}

        page_soup = BeautifulSoup(page, 'lxml')
        self._prime_block = page_soup.find('div', class_=Parser.PRIME_DIV_CLASS)
        if not self._prime_block:
            return {}
        self._get_img_def()
        self._get_name_morph_pronoun()
        self._get_examples()

        return self._description_dictionary

    def _get_img_def(self):
        """
        Parses 'src' of the image and the definition text and then adds them to self._description_dictionary 
        """
        img_def_block = self._prime_block.find('div', class_=Parser.IMG_DEF_DIV_CLASS)
        image = None
        definition = None
        # If block is still available and class name wasn't changed
        if img_def_block:
            # Only 'src' of the image is needed
            image = img_def_block.find('amp-img', class_=Parser.AMP_IMG_CLASS).get("src")
            definition = img_def_block.find('div', class_=Parser.DEF_DIV_CLASS)
            # There's no need in extra spaces and colons at the end
            definition = definition.text.strip()[:-1]
        if image:
            self._description_dictionary['image'] = image
        if definition:
            self._description_dictionary['definition'] = definition
        
    def _get_name_morph_pronoun(self):
        """
        Parses name text, morphology text and 'src' of pronunciations(UK, US).
        Then adds them to self._description_dictionary
        """
        name_morph_pronoun_block = self._prime_block.find('div', class_=Parser.NAME_MORPH_PRONOUN_DIV_CLASS)
        name = None
        morphology = None
        pronunciations = {}
        # If block is still available and class name wasn't changed
        if name_morph_pronoun_block:
            name = name_morph_pronoun_block.find('span', class_=Parser.NAME_SPAN_CLASS).text
            morphology = name_morph_pronoun_block.find('span', class_=Parser.MORPH_SPAN_CLASS).text
            # CED provides two ways of pronunciation(UK and US)
            pronunciations_raw = name_morph_pronoun_block.findAll('span', class_=Parser.PRONOUN_SPAN_CLASS)
            # Only 'src' of pronunciations are needed
            pronunciations['UK'] = pronunciations_raw[0].find('source').get('src')
            pronunciations['US'] = pronunciations_raw[1].find('source').get('src')
        if name:
            self._description_dictionary['name'] = name
        if morphology:
            self._description_dictionary['morphology'] = morphology
        if pronunciations:
            self._description_dictionary['pronunciations'] = pronunciations

    def _get_examples(self):
        """
        Parses examples text and then adds them to self._description_dictionary
        """
        # Max two first examples are needed
        examples = self._prime_block.findAll('li', class_=Parser.EXAMPLES_LI_CLASS, limit=2)
        # If block is still available and class name wasn't changed
        if examples:
            # Get only text from HTML code
            examples = [ex.text for ex in examples]
            self._description_dictionary['examples'] = examples


if __name__ == '__main__':
    result = Parser('apple').get_description()
    for key in result:
        print(key, ':', result[key])

