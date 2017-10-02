import random
import markovify
import string
import pprint
from sylco import sylco
import PyPDF2

# pdfFileObj = open('rape_corpus.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# page_nums = pdfReader.numPages

# def get_pdf_content(pdf_path, page_nums):
# 	content = ''
# 	p = file(pdf_path, "rb")
# 	pdf = PyPDF2.PdfFileReader(p)
# 	for page_num in range(page_nums):
# 		print page_num
# 		content += pdf.getPage(page_num).extractText()
# 	return content

# pdf_content = get_pdf_content("rape_corpus.pdf", page_nums )
# text_file = open('corpus/lyrics_batch.txt', 'w')  
# print pdf_content

def markov():
	with open('/Users/divyasingh/Documents/MABLE/Story_telling_lyrics/words/corpus/love_lyrics.txt') as f:
		text = f.read()
	reversed_lyrics = markovify.NewlineText(text)
	text_file = open('corpus/lyrics_batch.txt', 'w')  
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