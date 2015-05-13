#!cccenter/python/general.py
'''Grabs text from the Gutenberg Project to use as a plaintext.'''
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import random
import re

# Function that generates a random paragraph from a book.
def generate_paragraph():
    '''
    Generates a random paragraph from the Gutenberg Project

    :return: Text the Guttenberg Project with spaces and non-alphabetic characters removed\
    and all characters lower case
    :rtype: str
    '''
    #Get the text from Gutenberg Project, in this case its Moby Dick
    text = strip_headers(load_etext(2701)).strip()
    #text = "Jack and Jill ran up the hill to get a pail of water. " +
    #       "Jack fell down and broke his crown and Jill came tumbling after."
    sentences = []
    paragraph = ""

    for sentence in text.split("."):
        sentences.append(sentence)

    #Select 2 random sentences
    paragraph = random.choice(sentences) + random.choice(sentences)

    paragraph = re.sub(r'\s+', '', paragraph)
    regex = re.compile('[^a-zA-Z]')
    paragraph = regex.sub('', paragraph).lower()
    return paragraph

