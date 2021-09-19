import requests
from bs4 import BeautifulSoup
# CED - Cambridge English Dictionary


class Parser:
    """
    Class-parser. Processes Cambridge English Dictionary
    """
    # Cambridge English Dictionary URL
    CED_URL = 'https://dictionary.cambridge.org/dictionary/english/'
    CED_HOSTNAME = 'https://dictionary.cambridge.org'

    # Decrease the range of BS4 search by getting the common block to all needed data
    PRIME_DIV_CLASS = 'entry-body'

    # Image and word definition blocks
    AMP_IMG_CLASS = 'dimg_i'
    DEF_DIV_CLASS = 'def ddef_d db'

    # Name, morphology and pronunciations blocks
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
        image = None
        definition = None
        image = self._prime_block.find('amp-img', class_=Parser.AMP_IMG_CLASS)
        # Not every word has an image and thus, def_img_block could not exist
        definition = self._prime_block.find('div', class_=Parser.DEF_DIV_CLASS)
        # If blocks is still available and class name wasn't changed
        if image:
            # Only 'src' of the image is needed
            self._description_dictionary['image'] = self.CED_HOSTNAME + image.get('src')
        if definition:
            # There's no need in extra spaces
            definition = definition.text.strip()
            self._description_dictionary['definition'] = definition
        
    def _get_name_morph_pronoun(self):
        """
        Parses name text, morphology text and 'src' of pronunciations(UK, US).
        Then adds them to self._description_dictionary
        """
        name = None
        morphology = None
        pronunciations = {}
        name = self._prime_block.find('span', class_=Parser.NAME_SPAN_CLASS)
        morphology = self._prime_block.find('span', class_=Parser.MORPH_SPAN_CLASS)
        # CED provides two ways of pronunciation(UK and US)
        pronunciations_raw = self._prime_block.findAll('span', class_=Parser.PRONOUN_SPAN_CLASS)

        # If blocks are still available and class names weren't changed
        if name:
            self._description_dictionary['name'] = name.text
        if morphology:
            self._description_dictionary['morphology'] = morphology.text
        if pronunciations_raw:
            # If two pronunciations available
            if len(pronunciations_raw) > 1:
                # Only 'src' of pronunciations are needed
                first_pronunciation = pronunciations_raw[0].findAll('source')
                second_pronunciation = pronunciations_raw[1].findAll('source')

                # If search was success
                if first_pronunciation and second_pronunciation:
                    # First and second pronunciations consist .mp3 at [0] and .ogg at[1]
                    first_pronunciation = self.CED_HOSTNAME + first_pronunciation[1].get('src')
                    second_pronunciation = self.CED_HOSTNAME + second_pronunciation[1].get('src')

                    # To identify relevant pronunciation
                    if 'uk_pron' in first_pronunciation:
                        pronunciations['UK'] = first_pronunciation
                        pronunciations['US'] = second_pronunciation
                    else:
                        pronunciations['US'] = first_pronunciation
                        pronunciations['UK'] = second_pronunciation

            # If there's only one pronunciation
            elif len(pronunciations_raw) == 1:
                pronunciations = pronunciations_raw[0].find('source')
                if pronunciations:
                    pronunciations = self.CED_HOSTNAME + pronunciations.get('src')
            self._description_dictionary['pronunciations'] = pronunciations

    def _get_examples(self):
        """
        Parses examples[max 2] text and then adds them to self._description_dictionary
        """
        # Max two first examples are needed
        examples = self._prime_block.findAll('li', class_=Parser.EXAMPLES_LI_CLASS, limit=2)
        # If block is still available and class name wasn't changed
        if examples:
            # Get only text from HTML code
            examples = [ex.text for ex in examples]
            self._description_dictionary['examples'] = examples


if __name__ == '__main__':
    result = Parser('Junk').get_description()
    for key in result:
        print(key, ':', result[key])

