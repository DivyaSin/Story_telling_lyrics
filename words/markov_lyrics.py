import random
import markovify
import string
import pprint
from sylco import sylco

def markov():

	with open('/Users/divyasingh/Desktop/Story_telling_lyrics/words/corpus/love_lyrics.txt') as f:
		text = f.read()


# with open('/Users/divyasingh/Desktop/pywords-master/words/reversed_lyrics.txt') as f:
#     text = f.read()

	reversed_lyrics = markovify.NewlineText(text)
	text_file = open('corpus/lyrics_batch.txt', 'w')  
	for i in range(100):
    		text_file.write((reversed_lyrics.make_short_sentence(60)).translate(None, string.punctuation)+'.')
    		text_file.write("\n")
	text_file.close()


# Specify then remove punctuation
# punctuations = set([',','.','"','?','!'])

# def clean(sentence):
#     if sentence[-1] in punctuations:
#         return sentence[:-1]
#     return sentence

# def make_verse(verse_model):
#     verse = ''
#     stem = None

#     # Markovify for each line
#     for i in range():
#         while True:

#             line = verse_model.make_sentence()

#             if line is not None:

#                 syl_count = sylco(line)
#                 if syl_count > 16 or syl_count < 6:
#                     continue

#                 if i == 0:
#                     stem = clean(line.rsplit(None, 1)[-1])

#                 verse += (line + '\n')
#                 break

#     return verse

# def make_song(verse_model):

#     song = make_verse(verse_model)

#     return song

# print (make_song(reversed_lyrics))