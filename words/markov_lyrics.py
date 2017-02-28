import random
import markovify
import string
import pprint
from sylco import sylco

def markov():

	with open('/Users/divyasingh/Desktop/Story_telling_lyrics/words/corpus/love_lyrics.txt') as f:
		text = f.read()
	reversed_lyrics = markovify.NewlineText(text)
	text_file = open('corpus/lyrics_batch.txt', 'w')  
	for i in range(100):
    		text_file.write((reversed_lyrics.make_short_sentence(60)).translate(None, string.punctuation)+'.')
    		text_file.write("\n")
	text_file.close()