from collections import defaultdict
import nltk
from nltk.corpus import cmudict

rhyme_entries = nltk.corpus.cmudict.entries()
syllableWord = defaultdict( lambda: 1 )

for word, pronunciations in rhyme_entries:
    syllableWord[word] = len([x for x in pronunciations if x[-1].isdigit() ]) 

def syllables( word ):
    return syllableWord[word.lower()]

def sentence_syllables( sentence ):
    tokensInSentence = nltk.word_tokenize(sentence) 
    return sum( [ syllables(word) for word in tokensInSentence ] )
