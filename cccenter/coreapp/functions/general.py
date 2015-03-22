from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import random
import re

# Function that generates a random paragraph from a book.
def generate_paragraph():
	#Get the text from Gutenberg Project, in this case its Moby Dick
	text = strip_headers(load_etext(2701)).strip()
	sentences = []
	paragraph = ""

	for sentence in text.split("."):
		sentences.append(sentence)

	#Select 2 random sentences
	for i in range(2):
		sentence = random.choice(sentences)
		paragraph += sentence

	paragraph = re.sub(r'\s+', '', paragraph)	
	return paragraph