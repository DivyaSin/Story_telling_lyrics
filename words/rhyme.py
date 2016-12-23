import copy
import nltk
from collections import defaultdict
import random
import cPickle
import gzip
import os
import re
from nltk.corpus import PlaintextCorpusReader
import syllables
import pronouncing

rhyme_entries = nltk.corpus.cmudict.entries()

pronunciationDictionary = nltk.corpus.cmudict.dict() 



# output = ""
# file_name = "corpus/new_lyrics_reversed.txt"
# string_to_add = "."

# with open(file_name, 'r') as f:
#     file_lines = [''.join([x.strip(), string_to_add, '\n']) for x in f.readlines() ]

# with open(file_name, 'w') as f:
#     f.writelines(file_lines) 

corpus_root = '/Users/divyasingh/Desktop/Story_telling_lyrics/words/corpus'

wordlists = PlaintextCorpusReader(corpus_root, '.*')

# print wordlists.fileids()

# print wordlists.sents('lyrics1.txt')

# print wordlists.sents('lyrics.txt')

# li = [i.strip().split() for i in open("lyrics1.txt").readlines()]

# mega_sentences = ( wordlists.sents('taylor_lyrics.txt') ) 
mega_sentences = ( wordlists.sents('new_lyrics_reversed.txt') ) 

# mega_sentences = ( nltk.corpus.brown.sents() + 
#                 nltk.corpus.inaugural.sents() + 
#                 nltk.corpus.reuters.sents() + 
#                 nltk.corpus.webtext.sents() + 
#                 nltk.corpus.inaugural.sents() + 
#                 nltk.corpus.gutenberg.sents("carroll-alice.txt") +
#                 nltk.corpus.gutenberg.sents("austen-emma.txt") + 
#                 nltk.corpus.gutenberg.sents("austen-sense.txt") + 
#                 nltk.corpus.gutenberg.sents("blake-poems.txt") + 
#                 nltk.corpus.gutenberg.sents("bible-kjv.txt") + 
#                 nltk.corpus.gutenberg.sents("chesterton-ball.txt") + 
#                 nltk.corpus.gutenberg.sents("melville-moby_dick.txt") + 
#                 nltk.corpus.gutenberg.sents("milton-paradise.txt") + 
#                 nltk.corpus.gutenberg.sents("whitman-leaves.txt") + 
#                 nltk.corpus.gutenberg.sents("austen-persuasion.txt") + 
#                 nltk.corpus.gutenberg.sents("shakespeare-hamlet.txt") + 
#                 nltk.corpus.gutenberg.sents("shakespeare-macbeth.txt") ) 


last_word_sentences = defaultdict(list)

def last_word( sentence ):
    ss = [ word for word in sentence if len(word) > 1 ]
    if len(ss) > 0:
        return ss[-1]
    else:
        return "" 

if os.path.exists( "sentences.gz" ):
    with gzip.open( "sentences.gz", "r" ) as cache_file:
        last_word_sentences = cPickle.load( cache_file )
else:
    for sentence in mega_sentences:
        lw = last_word(sentence)
        last_word_sentences[ lw ].append(sentence)
    with gzip.open( "sentences.gz", "w") as cache_file:
        cPickle.dump(last_word_sentences, cache_file)

def candidate_sentences( word ):
    return last_word_sentences[ word.lower() ]

def qualityOfRhyme( p1, p2 ):
    p1 = copy.deepcopy(p1)
    # print p1
    p2 = copy.deepcopy(p2)
    # print p2
    p1.reverse()
    # print p1
    p2.reverse()
    # print p2
    if p1 == p2:
        return 0
    quality = 0
    for i, p in enumerate(p1):
        try:
            if p == p2[i]:
                quality += 1

            if p != p2[i]:
                break
        except IndexError:
            break
    return quality
    
def word_rhyme_candidates( word ):
    word = word.lower()
    candidates = []
    try:
        pronunciations = pronunciationDictionary[word]
    except KeyError:
        return word_rhyme_candidates(word[-1])

    if pronunciations == []:
        print "No pronunciations"
        return []

    for pronunciation in pronunciations:
        for rhyme_word, rhyme_pronunciation in rhyme_entries:
            quality = qualityOfRhyme(pronunciation, rhyme_pronunciation)
            if quality > 0:
                candidates.append( (quality, rhyme_word) )
    # print candidates
    candidates.sort()
    print "????????????????????????????????????????????????????"
    # print candidates
    candidates.reverse()
    print "####################################################"
    # print candidates



    # best_quality = candidates[0][0]
    # worst_quality = best_quality - 5
    # candidates = [ candidate for q, candidate in candidates if q >= worst_quality ]
    # print word
    # w = list(word)
    # w.reverse()
    # print w
    # the_vowel = ["a","e","i","o","u"]
    candidates = [ candidate for q, candidate in candidates ]
    # for cs in cs:
    #     findHighPriority(cs, word)

    # cd = [ candidate for q, candidate in candidates ]
    p2 = list(copy.deepcopy(word))
    p2.reverse()
    ls=[]

    for candidate in candidates:
        # print "$$$$$$$$$$$$$$$$$$$$$$$$"
        # print candidate
        p1 = list(copy.deepcopy(candidate))
        p1.reverse()
        # print "Words are:"
        # print p1
        # print p2
        if p1 == p2:
            return 0
        quality = 0
        sameVowelFound = False
        for i, p in enumerate(p1):
            try:
                if p == p2[i]:
                    # print p
                    # print p2[i]
                    quality += 1
                    if p in ('a', 'e', 'i', 'o', 'u') and (not sameVowelFound):
                        quality += 1
                        sameVowelFound = True
                    # print quality
                else:
                    break  
            except IndexError:
                break
        if quality > 0:
            ls.append( (quality, candidate) )

    # print "##############################"
    ls.sort()
    ls.reverse()
    # print ls
    new_candidates = [ ls for q, ls in ls ]
    # print candidates
    return new_candidates

def get_rhyme( sentence ):
    target_syllables = syllables.sentence_syllables( sentence )
    tokens = nltk.word_tokenize(sentence) 
    rhymes = word_rhyme_candidates(last_word(tokens))
    candidate_sentence = []
            
    # if len(tokens) == 1:
    #     return ", ".join(rhymes[:12])

    for rhyme in rhymes:
        candidate_sentence += candidate_sentences( rhyme )

    syllable_sentences = []

    for sentence in candidate_sentence:
        sumOfSyllables = sum( [ syllables.syllables(word) for word in sentence ] )
        syllable_sentences.append( (sumOfSyllables, " ".join(sentence)) )

    syllable_sentences.sort()
    syllable_sentences.reverse()
    
    if len( syllable_sentences ) == 0:
        if len( rhymes ) > 0: 
            return ", ".join(rhymes[:12])
        else:
            return "Oho ho ho ho ho"
    
    syllable_numbers = [ n for n, sentence in syllable_sentences ] 
    close_number = min( syllable_numbers, key=lambda x:abs(x-target_syllables) )
    
    close_sentences = [ sentence for n, sentence in syllable_sentences if close_number-6 <= n <= close_number+6 ] 

    return random.choice(close_sentences)

def generate_lyrics( string ):
    pat = ('\. +(?=[A-Z ])')
    text = re.sub(pat, '\n', string)
    print ""
    print ""
    print "##### STORY #####"
    print ""
    print text
    print ""
    print "#################"
    print 
    
    text_file = open('story.txt', 'w')  
    text_file.write(text)
    text_file.close()

    with open ("story.txt") as f:
        lines = f.readlines()
        line_no = 0
        rhyme_lines = []
        for line in lines:
            rhyme_line = get_rhyme(line)
            rhyme_lines.insert(line_no, rhyme_line)
            line_no += 1

    print "#### LYRICS ####"
    print ""
 
    for i, v in enumerate(rhyme_lines):
        lines.insert(2*i+1, v)

    for i,j in enumerate(lines):
        print j.strip("\n")
        if (i in [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47]):
            print ''
        else:
            pass
    print "################"

generate_lyrics("moon.")