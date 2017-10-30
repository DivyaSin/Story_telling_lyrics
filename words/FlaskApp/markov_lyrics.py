import markovify
import string

def markov():
	with open('/Users/divyasingh/Documents/MABLE/Story_telling_lyrics/words/corpus/love_lyrics.txt') as f:
		text = f.read()
	reversed_lyrics = markovify.NewlineText(text)
	text_file = open('/Users/divyasingh/Documents/MABLE/Story_telling_lyrics/words/corpus/lyrics_batch.txt', 'w')  
	for i in range(300):
		# print i
		sentence = reversed_lyrics.make_short_sentence(60)
		# print sentence
		if sentence:
			text_file.write(sentence.translate(None, string.punctuation) + '.')
			# text_file.write(sentence)
    		text_file.write("\n")
	text_file.close()

markov()