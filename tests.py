import unittest

import requests
from bs4 import BeautifulSoup

from parser import Parser


class URLTest(unittest.TestCase):

    def test_CED_URL_accessibility(self):
        user_agent = {'User-agent': 'Mozilla/5.0'}
        try:
            response = requests.get(Parser.CED_URL, headers=user_agent)
        except requests.exceptions.RequestException:
            self.fail("CED can't be reached")
        self.assertEqual(response.status_code, 200, 'CED_URL is no longer relevant')

    def test_CED_HOSTNAME_accessibility(self):
        user_agent = {'User-agent': 'Mozilla/5.0'}
        try:
            response = requests.get(Parser.CED_HOSTNAME, headers=user_agent)
        except requests.exceptions.RequestException:
            self.fail("CED can't be reached")
        self.assertEqual(response.status_code, 200, 'CED_HOSTNAME is no longer relevant')


class MarkupTest(unittest.TestCase):

    def test_PRIME_DIV_CLASS_relevance(self):
        test_word = 'apple'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        pars = Parser(test_word)
        response = requests.get(pars._url, headers=user_agent)
        page_soup = BeautifulSoup(response.text, 'lxml')
        prime_block = page_soup.find('div', class_=Parser.PRIME_DIV_CLASS)
        self.assertTrue(prime_block, 'PRIME_DIV_CLASS is no longer relevant')

    def test_AMP_IMG_CLASS_relevance(self):
        test_word = 'apple'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        pars = Parser(test_word)
        response = requests.get(pars._url, headers=user_agent)
        page_soup = BeautifulSoup(response.text, 'lxml')
        image_block = page_soup.find('amp-img', class_=Parser.AMP_IMG_CLASS)
        self.assertTrue(image_block, 'AMP_IMG_CLASS is no longer relevant')

    def test_DEF_DIV_CLASS_relevance(self):
        test_word = 'apple'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        pars = Parser(test_word)
        response = requests.get(pars._url, headers=user_agent)
        page_soup = BeautifulSoup(response.text, 'lxml')
        definition_block = page_soup.find('div', class_=Parser.DEF_DIV_CLASS)
        self.assertTrue(definition_block, 'DEF_DIV_CLASS is no longer relevant')

    def test_NAME_SPAN_CLASS_relevance(self):
        test_word = 'apple'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        pars = Parser(test_word)
        response = requests.get(pars._url, headers=user_agent)
        page_soup = BeautifulSoup(response.text, 'lxml')
        name_block = page_soup.find('span', class_=Parser.NAME_SPAN_CLASS)
        self.assertTrue(name_block, 'NAME_SPAN_CLASS is no longer relevant')

    def test_MORPH_SPAN_CLASS_relevance(self):
        test_word = 'apple'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        pars = Parser(test_word)
        response = requests.get(pars._url, headers=user_agent)
        page_soup = BeautifulSoup(response.text, 'lxml')
        morphology_block = page_soup.find('span', class_=Parser.MORPH_SPAN_CLASS)
        self.assertTrue(morphology_block, 'MORPH_SPAN_CLASS is no longer relevant')

    def test_PRONOUN_SPAN_CLASS_relevance(self):
        test_word = 'apple'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        pars = Parser(test_word)
        response = requests.get(pars._url, headers=user_agent)
        page_soup = BeautifulSoup(response.text, 'lxml')
        pronunciation_block = page_soup.find('span', class_=Parser.PRONOUN_SPAN_CLASS)
        self.assertTrue(pronunciation_block, 'PRONOUN_SPAN_CLASS is no longer relevant')

    def test_EXAMPLES_LI_CLASS_relevance(self):
        test_word = 'apple'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        pars = Parser(test_word)
        response = requests.get(pars._url, headers=user_agent)
        page_soup = BeautifulSoup(response.text, 'lxml')
        examples_block = page_soup.find('li', class_=Parser.EXAMPLES_LI_CLASS)
        self.assertTrue(examples_block, 'EXAMPLES_LI_CLASS is no longer relevant')


if __name__ == '__main__':
    unittest.main()
