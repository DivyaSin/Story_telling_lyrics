import random
import markovify
import string
import pprint
from sylco import sylco

def markov():
	with open('/Users/divyasingh/Documents/MABLE/rape_corpus.txt') as f:
		text = f.read()
	reversed_lyrics = markovify.NewlineText(text)
	text_file = open('corpus/lyrics_batch.txt', 'w')  
	for i in range(30):
		print i
		sentence = reversed_lyrics.make_short_sentence(60)
		print sentence
		if sentence:
			text_file.write(sentence.translate(None, string.punctuation)+'.')
    		text_file.write("\n")
	text_file.close()